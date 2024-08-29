# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base.billing import AbstactStripeSubscription


class StripeSubscription(AbstactStripeSubscription):
    customer = models.ForeignKey(
        "django_stripe.StripeCustomer",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )
