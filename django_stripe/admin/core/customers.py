# Third Party Stuff
from django.contrib import admin

# Django Stripe Stuff
from django_stripe.admin.abstracts import AbstractStripeModelAdmin
from django_stripe.models import StripeCustomer, StripeSubscription
from django_stripe.actions import StripeCustomerAction


class StripeSubscriptionInlineAdmin(admin.StackedInline):
    model = StripeSubscription
    extra = 0


@admin.register(StripeCustomer)
class StripeCustomerAdmin(AbstractStripeModelAdmin):
    list_display = (
        "stripe_id",
        "email",
        "name",
        "description",
        "is_active",
        "livemode",
        "deleted_at",
    )
    search_fields = ("stripe_id", "email", "name")
    inlines = [StripeSubscriptionInlineAdmin]
    stripe_model_action = StripeCustomerAction()
