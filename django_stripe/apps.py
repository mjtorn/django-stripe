# Third Party Stuff
import stripe
from django.apps import AppConfig

# Django Stripe Integrations Stuff
from django_stripe.settings import stripe_settings


class StripeIntegrationsConfig(AppConfig):
    name = "django_stripe"

    def ready(self):
        stripe.api_version = stripe_settings.API_VERSION
        stripe.api_key = stripe_settings.API_KEY
