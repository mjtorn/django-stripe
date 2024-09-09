# Third Party Stuff
import stripe
from django.apps import apps
from django.conf import settings

# Django Stripe Stuff
from django_stripe.actions.mixins import (
    StripeSoftDeleteActionMixin,
    StripeSyncActionMixin,
)
from django_stripe.models import StripeCustomer


class StripeCustomerAction(StripeSyncActionMixin, StripeSoftDeleteActionMixin):
    """
    Synchronizes a local StripeCustomer data from the Stripe API
    Syncing is done by retrieving a batch of customers from the Stripe API
    and then iterating over them and calling sync method on each of them.

    Example:
        from django_stripe.actions import StripeCustomerAction
        stripe_action = StripeCustomerAction()
        stripe_action.sync_all()
    """

    model_class = StripeCustomer
    stripe_object_class = stripe.Customer

    def post_set_default(self, defaults: dict):
        """
        Sets default values for stripe data
        Args:
            defaults: defaults data
        """
        user_model_class = apps.get_model(settings.AUTH_USER_MODEL)
        user = user_model_class.objects.filter(email=defaults["email"]).first()
        defaults["user"] = user
