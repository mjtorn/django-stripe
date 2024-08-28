# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base import (
    AbstactStripeCoupon,
    AbstactStripePrice,
    AbstactStripeProduct,
)


class StripeProduct(AbstactStripeProduct):
    pass


class StripePrice(AbstactStripePrice):
    price = models.ForeignKey(
        "django_stripe.StripeProduct",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )


class StripeCoupon(AbstactStripeCoupon):
    pass
