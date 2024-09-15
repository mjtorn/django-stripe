# Third Party Stuff
import stripe

# Django Stripe Stuff
from django_stripe.actions.core import StripeCustomer
from django_stripe.actions.mixins import (
    StripeSoftDeleteActionMixin,
    StripeSyncActionMixin,
)
from django_stripe.models import StripeSubscription


class StripeSubscriptionAction(StripeSyncActionMixin, StripeSoftDeleteActionMixin):
    """
    Synchronizes a local StripeSubscription data from the Stripe API

    Syncing is done by retrieving a batch of subscriptions from the Stripe API
    and then iterating over them and calling sync method on each of them.

    Example:
        from django_stripe.actions import StripeSubscriptionAction
        stripe_action = StripeSubscriptionAction()
        stripe_action.sync_all()
    """

    model_class = StripeSubscription
    stripe_object_class = stripe.Subscription

    def pre_set_defualt(self, stripe_data: dict):
        """
        Add customer data to stripe_data
        """
        stripe_data["customer"] = StripeCustomer.objects.get(
            stripe_id=stripe_data["customer"]
        )
