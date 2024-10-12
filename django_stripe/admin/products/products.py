# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripeProduct, StripePrice
from django_stripe.actions import StripeProductAction


class StripePriceInlineAdmin(admin.StackedInline):
    model = StripePrice
    extra = 0


@admin.register(StripeProduct)
class StripeProductAdmin(AbstractStripeModelAdmin):
    list_display = ("stripe_id", "name", "description")
    search_fields = ("stripe_id", "name", "description")
    inlines = [StripePriceInlineAdmin]
    stripe_model_action = StripeProductAction()
