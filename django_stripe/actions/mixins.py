# Third Party Stuff
from django.utils import timezone

# Django Stripe Stuff
from django_stripe.utils import convert_epoch


class StripeSoftDeleteActionMixin:
    """
    A mixin class that provides a soft_delete method which allows to soft delete
    local stripe objects. This is useful when you want to mark a stripe object as
    deleted without actually deleting it in the local database.

    Example:
        from django_stripe.actions import StripeSoftDeleteActionMixin
        from django_stripe.models import StripeCustomer

        class StripeCustomerAction(StripeSoftDeleteActionMixin):
            model_class = StripeCustomer

        stripe_action = StripeCustomerAction()
        stripe_action.soft_delete("cus_123456789")
    """

    model_class = None

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
    """
    A mixin class that provides a sync method that synchronizes a local
    data from the Stripe API

    Syncing is done by retrieving a batch of objects from the Stripe API
    and then iterating over them and calling sync method on each of them.

    Example:
        from django_stripe.actions import StripeSyncActionMixin
        from django_stripe.models import StripeCustomer

        class StripeCustomerAction(StripeSyncActionMixin):
            model_class = StripeCustomer

        stripe_action = StripeCustomerAction()
        stripe_action.sync_all()
    """

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

    def post_set_default(self, defaults: dict):
        """
        Override this method to perform actions after setting the default.
        """
        pass

    def set_default(self, stripe_data: dict):
        defaults = {}

        for field in self.model_class._meta.get_fields():
            if field.name not in stripe_data:
                continue

            field_type = field.get_internal_type()

            if field_type == "DateTimeField":
                defaults[field.name] = (
                    convert_epoch(stripe_data[field.name])
                    if stripe_data[field.name]
                    else None
                )
            elif field_type in ["CharField", "TextField"]:
                defaults[field.name] = stripe_data[field.name] or ""
            else:
                defaults[field.name] = stripe_data[field.name]

        return defaults

    def sync(self, stripe_data: dict):
        """
        Synchronizes a local data from the Stripe API
        Args:
            stripe_data: data from Stripe API
        """

        self.pre_set_defualt(stripe_data)
        stripe_id = stripe_data.pop("id")
        defaults = self.set_default(stripe_data)
        self.post_set_default(defaults)

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
        if not model_objs:
            return

        for model_obj in model_objs:
            stripe_id = model_obj.stripe_id
            data = stripe_id_obj_map[stripe_id]

            self.pre_set_defualt(data)
            defaults = self.set_default(data)
            self.post_set_default(defaults)

            for key, value in defaults.items():
                setattr(model_obj, key, value)

            del stripe_id_obj_map[stripe_id]

        self.model_class.objects.bulk_update(model_objs, fields=list(defaults.keys()))

    def _create_model_objs(self, stripe_id_obj_map: dict[str, dict]):
        """
        Creates model objects
        Args:
            stripe_id_obj_map: dict of stripe id and stripe object data to be created
        """
        if not stripe_id_obj_map:
            return

        model_objs = []

        for stripe_id, data in stripe_id_obj_map.items():
            self.pre_set_defualt(data)
            defaults = self.set_default(data)
            defaults["stripe_id"] = stripe_id
            self.post_set_default(defaults)

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

        self.sync_batch(batch)

        # sync deleted objects
        self.model_class.objects.exclude(stripe_id__in=stripe_ids).update(
            date_purged=timezone.now()
        )
