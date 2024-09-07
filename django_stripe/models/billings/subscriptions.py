# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.billings import AbstractStripeSubscription


class StripeSubscription(AbstractStripeSubscription):
    customer = models.ForeignKey(
        "django_stripe.StripeCustomer",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )
