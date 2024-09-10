# Third Party Stuff
from django.dispatch import Signal


class WebhookRegistry(object):
    """
    WebhookRegistry is a class that registers webhooks.

    Webhooks are real-time notifications that are sent to your application
    when events happen in your Stripe account. For example, when a subscription
    is created, a webhook is sent to your application. You can then use this webhook
    to run actions in your application.

    WebhookRegistry is designed to be used with django. It provides a simple way to
    register webhook events in your application.

    Example:
        from django_stripe.webhooks import WebhookRegistry

        webhook_registry = WebhookRegistry()
        webhook_registry.register(PaymentSucceededWebhook)

        # process webhook events
        webhook_registry.process_webhook(
            {"id": "evt_123456789", "type": "payment_succeeded"}
        )

        # process webhook events from stripe
        webhook_registry.process_webhook(stripe.Event.retrieve("evt_123456789"))
    """

    def __init__(self):
        self._registry = {}

    def register(self, webhook):
        self._registry[webhook.name] = {
            "webhook": webhook,
            "signal": Signal(providing_args=["event"]),
        }

    def keys(self):
        return self._registry.keys()

    def get(self, name, default=None):
        try:
            return self[name]["webhook"]
        except KeyError:
            return default

    def get_signal(self, name, default=None):
        try:
            return self[name]["signal"]
        except KeyError:
            return default

    def signals(self):
        return {key: self.get_signal(key) for key in self.keys()}

    def __getitem__(self, name):
        return self._registry[name]
