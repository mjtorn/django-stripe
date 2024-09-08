# Third Party Stuff
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Django Stripe Stuff
from django_stripe.models import StripeCustomer, StripeEvent


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
        from django_stripe.webhooks.register import registry

        WebhookClass = registry.get(kind)
        if WebhookClass is not None:
            webhook = WebhookClass(event)
            webhook.process()

    def link_customer(self, event):
        """
        Links a customer referenced in a webhook event message to the event object
        Args:
            event: the django_stripe.stripe.models.Event object to link
        """

        if event.kind == "customer.created":
            return

        customer_crud_events = [
            "customer.updated",
            "customer.deleted",
        ]
        event_data_object = event.message["data"]["object"]
        if event.kind in customer_crud_events:
            stripe_customer_id = event_data_object["id"]
        else:
            stripe_customer_id = event_data_object.get("customer", None)

        if stripe_customer_id is not None:
            try:
                customer = StripeCustomer.objects.get(stripe_id=stripe_customer_id)
            except ObjectDoesNotExist:
                raise Http404(
                    f"Stripe customer does not exist for event={event.stripe_id}"
                )

            event.customer = customer
            event.save()

        return event
