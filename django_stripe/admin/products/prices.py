# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripePrice
from django_stripe.actions import StripePriceAction


@admin.register(StripePrice)
class StripePriceAdmin(AbstractStripeModelAdmin):
    list_display = ("stripe_id", "nickname", "type", "active", "livemode", "deleted_at")
    search_fields = ("stripe_id", "nickname", "type")
    list_filter = ("type", "active")
    stripe_model_action = StripePriceAction()
