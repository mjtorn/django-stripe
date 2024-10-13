# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripeSubscription
from django_stripe.actions import StripeSubscriptionAction


@admin.register(StripeSubscription)
class StripeSubscriptionAdmin(AbstractStripeModelAdmin):
    list_display = ("stripe_id", "start_date", "status", "livemode", "deleted_at")
    search_fields = ("stripe_id",)
    list_filter = ("status", "start_date")
    stripe_model_action = StripeSubscriptionAction()
