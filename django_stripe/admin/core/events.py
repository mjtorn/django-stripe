# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripeEvent
from django_stripe.actions import StripeEventAction


@admin.register(StripeEvent)
class StripeEventAdmin(AbstractStripeModelAdmin):
    list_display = ("stripe_id", "api_version", "kind", "valid", "processed")
    search_fields = ("stripe_id", "kind")
    stripe_model_action = StripeEventAction()
