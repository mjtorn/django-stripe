# Django Stripe Stuff
from django_stripe.actions import StripeProductAction
from django_stripe.webhooks.register import StripeWebhook


class ProductStripeWebhook(StripeWebhook):
    def process_webhook(self):
        if self.event.validated_message:
            StripeProductAction().sync(
                self.event.validated_message["data"]["object"].copy()
            )


class ProductCreatedWebhook(ProductStripeWebhook):
    name = "product.created"
    description = "Occurs whenever a new product is created."


class ProductUpdatedWebhook(ProductStripeWebhook):
    name = "product.updated"
    description = "Occurs whenever any property of a product changes."


class ProductDeletedWebhook(StripeWebhook):
    name = "product.deleted"
    description = "Occurs whenever a product is deleted."

    def process_webhook(self):
        StripeProductAction().soft_delete(
            self.event.validated_message["data"]["object"]["id"]
        )
