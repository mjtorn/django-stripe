# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.core import AbstractStripeEvent


class StripeEvent(AbstractStripeEvent):
    customer = models.ForeignKey(
        "django_stripe.StripeCustomer",
        to_field="stripe_id",
        on_delete=models.SET_NULL,
        null=True,
        related_name="events",
    )
