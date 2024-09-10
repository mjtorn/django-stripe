# Third Party Stuff
import stripe

# Django Stripe Stuff
from django_stripe.actions.mixins import (
    StripeSoftDeleteActionMixin,
    StripeSyncActionMixin,
)
from django_stripe.models import StripeCoupon, StripePrice, StripeProduct


class StripeProductAction(StripeSyncActionMixin, StripeSoftDeleteActionMixin):
    """
    Actions related to products in Stripe that can be used for various purposes.

    Syncing is done by retrieving a batch of products from the Stripe API
    and then iterating over them and calling sync method on each of them.

    Example:
        from django_stripe.actions import StripeProductAction

        StripeProductAction.sync_all()
    """

    model_class = StripeProduct
    stripe_object_class = stripe.Product


class StripePriceAction(StripeSyncActionMixin, StripeSoftDeleteActionMixin):
    product_model_class = StripeProduct
    stripe_product_class = stripe.Product
    model_class = StripePrice
    stripe_object_class = stripe.Product

    def pre_set_defualt(self, stripe_data: dict):
        """
        Sync product if not exist.
        Update product field with product object
        Args:
            stripe_data: data from Stripe API representing a price
        """
        product = self.product_model_class.objects.filter(
            stripe_id=stripe_data["product"]
        ).first()

        if not product:
            stripe_product = self.stripe_product_class.retrieve(stripe_data["product"])
            product = StripeProductAction().sync(stripe_product)

        stripe_data["product"] = product


class StripeCouponAction(StripeSoftDeleteActionMixin, StripeSyncActionMixin):
    model_class = StripeCoupon
    stripe_object_class = stripe.Coupon
