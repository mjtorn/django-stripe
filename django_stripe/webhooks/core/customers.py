# Third Party Stuff
from django.apps import apps
from django.conf import settings

# Django Stripe Stuff
from django_stripe.actions import StripeCustomerAction
from django_stripe.models import StripeCustomer
from django_stripe.webhooks.register import StripeWebhook


class CustomerUpdatedWebhook(StripeWebhook):
    name = "customer.updated"
    description = "Occurs whenever any property of a customer changes."

    def process_webhook(self):
        if self.event.customer:
            stripe_customer = self.event.message["data"]["object"].copy()
            StripeCustomerAction().sync(stripe_customer)


class CustomerCreatedWebhook(StripeWebhook):
    name = "customer.created"
    description = "Occurs whenever a new customer is created."

    def process_webhook(self):
        stripe_customer = self.event.message["data"]["object"]
        email = stripe_customer["email"]
        stripe_id = self.event.message["data"]["object"]["id"]
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User.objects.filter(email=email).first()

        if user and not user.stripe_customers.exists():
            # create customer
            data = {
                "user": user,
                "email": user.email,
                "is_active": True,
                "defaults": {"stripe_id": stripe_id},
            }
            customer, _ = StripeCustomer.objects.get_or_create(**data)

            # link customer to event
            self.event.customer = customer
            self.event.save()

            # sync customer
            StripeCustomerAction().sync(stripe_customer)


class CustomerDeletedWebhook(StripeWebhook):
    name = "customer.deleted"
    description = "Occurs whenever a customer is deleted."

    def process_webhook(self):
        if self.event.customer:
            StripeCustomerAction().soft_delete(self.event.customer.stripe_id)
