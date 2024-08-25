# Django Stripe Stuff
from django_stripe.settings import stripe_settings


class StripeRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migration only for the 'StripeCustomer' model
        if app_label == "django_stripe" and (
            "__all__" in stripe_settings.ALLOWED_MODELS
            or model_name in stripe_settings.ALLOWED_MODELS
        ):
            return True
        return False
