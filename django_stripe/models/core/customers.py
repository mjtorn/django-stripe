# Third Party Stuff
from django.conf import settings
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.core import AbstractStripeCustomer


class StripeCustomer(AbstractStripeCustomer):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stripe_customers",
    )
