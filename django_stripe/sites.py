# Third Party Stuff
from django.contrib.admin import AdminSite
from django.db.models.base import ModelBase

# Django Stripe Stuff
from django_stripe.settings import stripe_settings


class StripeAdminSite(AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        if "__all__" in stripe_settings.ALLOWED_ADMIN_MODELS:
            super().register(model_or_iterable, admin_class, **options)

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        # Filter models that are allowed to be registered
        allowed_model_or_iterable = []
        for model in model_or_iterable:
            if model._meta.model_name in stripe_settings.ALLOWED_ADMIN_MODELS:
                allowed_model_or_iterable.append(model)

        super().register(allowed_model_or_iterable)
