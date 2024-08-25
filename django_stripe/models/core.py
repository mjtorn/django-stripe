# Django Stripe Stuff
from django_stripe.models.base.core import StripeBaseCustomer, StripeBaseEvent


class StripeCustomer(StripeBaseCustomer):
    pass


class StripeEvent(StripeBaseEvent):
    pass
