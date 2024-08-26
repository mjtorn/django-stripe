# Third Party Stuff
import stripe
from django.apps import AppConfig

# Django Stripe Stuff
from django_stripe.settings import stripe_settings


class DjangoStripeConfig(AppConfig):
    name = "django_stripe"

    def ready(self):
        if stripe_settings.API_VERSION:
            stripe.api_version = stripe_settings.API_VERSION
        stripe.api_key = stripe_settings.API_KEY
