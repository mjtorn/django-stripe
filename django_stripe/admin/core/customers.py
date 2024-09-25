from django.contrib import admin
from django_stripe.models import StripeCustomer


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ("stripe_id", "email", "name", "description")
    search_fields = ("stripe_id", "email", "name", "description")
