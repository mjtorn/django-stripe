# Django Stripe Stuff
from django_stripe.actions import StripeCardAction
from django_stripe.webhooks.register import StripeWebhook


class CustomerCardStripeWebhook(StripeWebhook):
    def process_webhook(self):
        StripeCardAction().sync(
            self.event.customer, self.event.validated_message["data"]["object"]
        )


class CustomerCardCreatedWebhook(CustomerCardStripeWebhook):
    name = "customer.source.created"
    description = "Occurs whenever a new source is created for the customer."


class CustomerCardDeletedWebhook(StripeWebhook):
    name = "customer.source.deleted"
    description = "Occurs whenever a source is removed from a customer."

    def process_webhook(self):
        StripeCardAction().delete(self.event.validated_message["data"]["object"]["id"])


class CustomerCardUpdatedWebhook(CustomerCardStripeWebhook):
    name = "customer.source.updated"
    description = "Occurs whenever a source's details are changed."
