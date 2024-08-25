from django.db import models

# Django Stripe Stuff
from django_stripe.models import (
    StripeBaseCard,
    StripeBaseCoupon,
    StripeBaseSubscription,
    StripeBaseProduct,
    StripeBaseEvent,
    StripeBaseCustomer,
    StripeBasePrice,
)


# Create your models here.
class StripeCustomer(StripeBaseCustomer):
    pass


class StripeCard(StripeBaseCard):
    customer = models.ForeignKey(StripeCustomer, to_field="stripe_id")


class StripeProduct(StripeBaseProduct):
    pass


class StripePrice(StripeBasePrice):
    product = models.ForeignKey(StripeProduct, to_field="stripe_id")


class StripeEvent(StripeBaseEvent):
    pass


class StripeSubscription(StripeBaseSubscription):
    price = models.ForeignKey(StripePrice, to_field="stripe_id")


class StripeCoupon(StripeBaseCoupon):
    pass
