# Django Stripe Stuff
from django_stripe.actions import StripeCustomerAction, StripeSubscriptionAction
from django_stripe.webhooks.register import StripeWebhook


class CustomerSubscriptionStripeWebhook(StripeWebhook):
    def process_webhook(self):
        if self.event.validated_message:
            StripeSubscriptionAction(self.event.customer.stripe_id).sync(
                self.event.validated_message["data"]["object"],
            )

        if self.event.customer:
            StripeCustomerAction.sync(self.event.customer)


class CustomerSubscriptionCreatedWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.created"
    description = (
        "Occurs whenever a customer with no subscription is signed up for a plan."
    )


class CustomerSubscriptionDeletedWebhook(CustomerSubscriptionStripeWebhook):
    name = "customer.subscription.deleted"
    description = "Occurs whenever a customer ends their subscription."


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
