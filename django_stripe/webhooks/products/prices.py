# Django Stripe Stuff
from django_stripe.actions import StripePriceAction
from django_stripe.webhooks.register import StripeWebhook


class PriceStripeWebhook(StripeWebhook):
    def process_webhook(self):
        StripePriceAction().sync(self.event.message["data"]["object"])


class PriceCreatedWebhook(PriceStripeWebhook):
    name = "price.created"
    description = "Occurs whenever a new price is created."


class PriceUpdatedWebhook(PriceStripeWebhook):
    name = "price.updated"
    description = "Occurs whenever any property of a price changes."


class PriceDeletedWebhook(PriceStripeWebhook):
    name = "price.deleted"
    description = "Occurs whenever a price is deleted."

    def process_webhook(self):
        StripePriceAction().soft_delete(
            self.event.validated_message["data"]["object"]["id"]
        )
