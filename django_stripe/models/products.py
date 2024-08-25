# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base.products import StripeBasePrice, StripeBaseProduct


class StripeProduct(StripeBaseProduct):
    pass


class StripePrice(StripeBasePrice):
    price = models.ForeignKey(
        "django_tripe.StripeProduct",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )
