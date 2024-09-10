# Standard Library
import logging

# Third Party Stuff
from django.utils.encoding import smart_str
from stripe.error import InvalidRequestError

# Django Stripe Stuff
from django_stripe.actions import StripeEventAction
from django_stripe.models import StripeEvent

logger = logging.getLogger(__name__)


class StripeWebhook:
    """
    StripeWebhook is a class that processes stripe webhooks.

    Stripe webhooks are real-time notifications that are sent to your application
    when events happen in your stripe account. For example, when a subscription
    is created, a webhook is sent to your application. You can then use this webhook
    to run actions in your application.

    StripeWebhook is designed to be used with django. It provides a simple way to
    process webhook events in your application.

    Example:
        from django_stripe.actions import StripeWebhook
        from django_stripe.webhooks import PaymentSucceededWebhook

        webhook = StripeWebhook()
        webhook.register(PaymentSucceededWebhook)

        # process webhook events
        webhook.process_webhook({"id": "evt_123456789", "type": "payment_succeeded"})

        # process webhook events from stripe
        webhook.process_webhook(stripe.Event.retrieve("evt_123456789"))
    """

    @classmethod
    def process_webhook(cls, event_data):
        event = StripeEvent.objects.filter(stripe_id=event_data["id"]).first()

        if event:
            logger.info(
                "Found duplicate stripe event record with event_id=%s", event.id
            )
            return

        try:
            # create an event and process webhook
            StripeEventAction.add(
                stripe_id=event_data["id"],
                kind=event_data["type"],
                livemode=event_data["livemode"],
                message=event_data,
                api_version=event_data["api_version"],
                request=event_data["request"],
                pending_webhooks=event_data["pending_webhooks"],
            )
        except InvalidRequestError as e:
            event_id = event_data["id"]
            logger.info(
                "Error occurred while processing stripe webhook, "
                f"event_id={event_id}, error={smart_str(e)}"
            )
        return
