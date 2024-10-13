# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripeCoupon
from django_stripe.actions import StripeCouponAction


@admin.register(StripeCoupon)
class StripeCouponAdmin(AbstractStripeModelAdmin):
    list_display = ("stripe_id", "name", "valid", "livemode", "deleted_at")
    search_fields = ("stripe_id", "name")
    list_filter = ("valid",)
    stripe_model_action = StripeCouponAction()
