# Third Party Stuff
import stripe

# Django Stripe Stuff
from django_stripe.actions.mixins import StripeSyncActionMixin
from django_stripe.models import StripeCard


class StripeCardAction(StripeSyncActionMixin):
    model_class = StripeCard

    def __init__(self, customer):
        """
        Args:
            customer: django-stripe Customer
        """
        self.customer = customer

    def pre_set_defualt(self, stripe_data: dict):
        """
        Add customer data to stripe_data
        """
        stripe_data["customer"] = self.customer.stripe_id

    def delete(self, stripe_id):
        """
        Deletes a card from a customer
        Args:
            source_stripe_id: the Stripe ID of the payment source to delete
        Ref Docs: https://stripe.com/docs/api/cards/delete
        """
        stripe.Customer.delete_source(self.customer.stripe_id, stripe_id)
        return self.model_class.objects.filter(stripe_id=stripe_id).delete()
