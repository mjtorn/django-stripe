# Third Party Stuff
import stripe

# Django Stripe Stuff
from django_stripe.actions.core import StripeCustomer
from django_stripe.actions.mixins import StripeSyncActionMixin
from django_stripe.models import StripeSubscription


class StripeSubscriptionAction(StripeSyncActionMixin):
    model_class = StripeSubscription
    stripe_object_class = stripe.Subscription

    def __init__(self, stripe_customer_id):
        """
        Args:
            customer: the customer to create the subscription for
        """
        self.customer = StripeCustomer.objects.get(stripe_id=stripe_customer_id)

    def pre_set_defualt(self, stripe_data: dict):
        """
        Add customer data to stripe_data
        """
        stripe_data["customer"] = self.customer
