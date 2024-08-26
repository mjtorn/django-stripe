# Django Stripe Stuff
from django_stripe.models import StripeEvent


class StripeEventAction:
    @classmethod
    def add(
        cls,
        stripe_id,
        kind,
        livemode,
        api_version,
        message,
        request=None,
        pending_webhooks=0,
    ):
        """
        Adds and processes an event from a received webhook
        Args:
            stripe_id: the stripe id of the event
            kind: the label of the event
            livemode: True or False if the webhook was sent from livemode or not
            message: the data of the webhook
            request_id: the id of the request that initiated the webhook
            pending_webhooks: the number of pending webhooks
        """
        event = StripeEvent.objects.create(
            stripe_id=stripe_id,
            kind=kind,
            livemode=livemode,
            webhook_message=message,
            api_version=api_version,
            request=request,
            pending_webhooks=pending_webhooks,
        )

        # Django Stripe Stuff
        from django_stripe.webhooks.base import registry

        WebhookClass = registry.get(kind)
        if WebhookClass is not None:
            webhook = WebhookClass(event)
            webhook.process()
