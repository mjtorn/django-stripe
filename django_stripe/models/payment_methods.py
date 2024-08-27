# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base.payment_methods import StripeBaseCard


class StripeCard(StripeBaseCard):
    customer = models.ForeignKey(
        "django_stripe.StripeCustomer",
        to_field="stripe_id",
        on_delete=models.CASCADE,
        null=True,
    )
