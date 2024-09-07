# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts import AbstractStripePrice


class StripePrice(AbstractStripePrice):
    product = models.ForeignKey(
        "django_stripe.StripeProduct",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )
