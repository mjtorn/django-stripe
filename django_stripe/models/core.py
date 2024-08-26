# Third Party Stuff
from django.conf import settings
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base.core import StripeBaseCustomer, StripeBaseEvent


class StripeCustomer(StripeBaseCustomer):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )


class StripeEvent(StripeBaseEvent):
    pass
