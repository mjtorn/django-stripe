# Third Party Stuff
from django.utils import timezone


class StripeSoftDeleteActionMixin:
    def soft_delete(self, stripe_id: str):
        """
        Deletes the local stripe object
        Args:
            stripe_id: the Stripe ID of the stripe object
        """
        obj = self.model_class.objects.filter(stripe_id=stripe_id).first()
        if obj:
            obj.date_purged = timezone.now()
            obj.save()


class StripeSyncActionMixin:
    model_class = None
    stripe_object_class = None
    batch_size = 1000

    def pre_set_defualt(self, stripe_data: dict):
        """
        Override this method to set values in stripe_data
        before setting the default.
        Or perform certain actions before setting the default.
        Args:
            stripe_data: data from Stripe API
        """
        pass

    def post_set_default(self):
        """
        Override this method to perform actions after setting the default.
        """
        pass

    def set_default(self, stripe_data: dict):
        model_fields = set(self.model_class._meta.fields)
        return {key: value for key, value in stripe_data.items() if key in model_fields}

    def sync(self, stripe_data: dict):
        """
        Synchronizes a local data from the Stripe API
        Args:
            stripe_data: data from Stripe API
        """

        self.pre_set_defualt(stripe_data)
        stripe_id = stripe_data.pop("id")
        defaults = self.set_default(stripe_data)

        model_obj, _ = self.model_class.objects.update_or_create(
            stripe_id=stripe_id, defaults=defaults
        )

        return model_obj

    def sync_by_ids(self, ids):
        """
        Synchronizes a local data from the Stripe API
        Args:
            ids: list of ids
        """
        stripe_data = self.stripe_object_class.retrieve(ids)
        self.sync(stripe_data)

    def _update_model_objs(
        self, model_objs: list[object], stripe_id_obj_map: dict[str, dict]
    ):
        """
        Updates model objects
        Args:
            model_objs: list of model objects
            stripe_id_obj_map: dict of stripe id and stripe object data to be updated
        """
        for model_obj in model_objs:
            stripe_id = model_obj.stripe_id
            data = stripe_id_obj_map[stripe_id]

            data.pop("id")
            self.pre_set_defualt(data)
            defaults = self.set_default(data)

            for key, value in defaults.items():
                setattr(model_obj, key, value)

            del stripe_id_obj_map[stripe_id]

    def _create_model_objs(self, stripe_id_obj_map: dict[str, dict]):
        """
        Creates model objects
        Args:
            stripe_id_obj_map: dict of stripe id and stripe object data to be created
        """
        model_objs = []

        for stripe_id, data in stripe_id_obj_map.items():
            self.pre_set_defualt(data)

            data.pop("id")
            self.pre_set_defualt(data)
            defaults = self.set_default(data)
            defaults["stripe_id"] = stripe_id

            model_objs.append(self.model_class(**defaults))

        self.model_class.objects.bulk_create(model_objs)

    def sync_batch(self, batch: list[dict]):
        """
        Synchronizes a batch of data from the Stripe API
        Args:
            batch: list of data from Stripe API
        """
        stripe_id_obj_map = {}
        for data in batch:
            stripe_id = data.pop("id")
            stripe_id_obj_map[stripe_id] = data

        model_objs = self.model_class.objects.filter(
            stripe_id__in=stripe_id_obj_map.keys()
        )
        self._update_model_objs(model_objs, stripe_id_obj_map)
        self._create_model_objs(stripe_id_obj_map)

    def sync_all(self):
        """
        Synchronizes all data from the Stripe API
        """
        objects = self.stripe_object_class.auto_paging_iter()
        stripe_ids = []
        batch = []

        for i, obj in enumerate(objects):
            stripe_ids.append(obj["id"])
            batch.append(obj)
            if (i + 1) % self.batch_size == 0:
                self.sync_batch(batch)
                batch = []

        # sync deleted objects
        self.model_class.objects.exclude(stripe_id__in=stripe_ids).update(
            date_purged=timezone.now()
        )
