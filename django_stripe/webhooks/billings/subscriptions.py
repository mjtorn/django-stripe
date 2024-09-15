# Django Stripe Stuff
from django_stripe.actions import StripeSubscriptionAction
from django_stripe.webhooks.register import StripeWebhook


class CustomerSubscriptionStripeWebhook(StripeWebhook):
    def process_webhook(self):
        if self.event.validated_message:
            StripeSubscriptionAction().sync(
                self.event.validated_message["data"]["object"].copy(),
            )


class CustomerSubscriptionCreatedWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.created"
    description = (
        "Occurs whenever a customer with no subscription is signed up for a plan."
    )


class CustomerSubscriptionDeletedWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.deleted"
    description = "Occurs whenever a customer ends their subscription."

    def process_webhook(self):
        if self.event.validated_message:
            StripeSubscriptionAction().soft_delete(
                self.event.validated_message["data"]["object"]["id"]
            )


class CustomerSubscriptionTrialWillEndWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.trial_will_end"
    description = (
        "Occurs three days before the trial "
        "period of a subscription is scheduled to end."
    )


class CustomerSubscriptionUpdatedWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.updated"
    description = (
        "Occurs whenever a subscription changes. "
        "Examples would include switching from one plan to another, "
        "or switching status from trial to active."
    )
