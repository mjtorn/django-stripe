# Third Party Stuff
import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Django Stripe Stuff
from django_stripe import utils
from django_stripe.actions.mixins import StripeSoftDeleteActionMixin
from django_stripe.models import StripeCustomer


class StripeCustomerAction(StripeSoftDeleteActionMixin):
    def __init__(self, user):
        self.user = user

    def create(self, billing_email, metadata=None, **kwargs):
        """
        Creates a Stripe customer.
        If a customer already exists, the existing customer will be returned.
        Args:
            billing_email: email address to bind the customer to
            metadata: dict of metadata to attach to the customer
            kwargs: additional kwargs to pass to stripe.Customer.create
        Returns:
            a customer object that was created
        """
        if not metadata:
            metadata = {}

        customer = self.get()
        if customer:
            try:
                stripe.Customer.retrieve(customer.stripe_id)
                return customer
            except stripe.error.InvalidRequestError:
                pass

        # At this point we maybe have a local Customer but no stripe customer
        # let's create one and make the binding
        stripe_customer = stripe.Customer.create(
            email=billing_email, metadata=metadata, **kwargs
        )

        data = {
            "user": self.user,
            "is_active": True,
            "livemode": stripe_customer["livemode"],
            "defaults": {"stripe_id": stripe_customer["id"], "email": billing_email},
        }

        customer, created = StripeCustomer.objects.get_or_create(**data)

        if not created:
            customer.stripe_id = stripe_customer["id"]  # sync will call customer.save()

        customer = self.sync_from_stripe_data(customer, stripe_customer)

        return customer

    def get(self):
        """
        Get a customer object for a given user
        Returns:
            a django_stripe.StripeCustomer object
        """
        data = {"user": self.user, "is_active": True}
        customer = StripeCustomer.objects.filter(**data).first()

        return customer

    def sync_from_stripe_data(self, customer, stripe_customer):
        """
        Synchronizes a local Customer object with details from the Stripe API
        Args:
            customer: a Customer object
            stripe_customer: optionally,
            data from the Stripe API representing the customer
        Returns:
            a django_stripe.StripeCustomer object
        """
        customer.balance = utils.convert_amount_for_db(
            stripe_customer["balance"], stripe_customer["currency"]
        )
        customer.currency = stripe_customer["currency"] or ""
        customer.delinquent = stripe_customer["delinquent"]
        customer.default_source = stripe_customer["default_source"] or ""
        customer.description = stripe_customer["description"] or ""
        customer.address = stripe_customer["address"] or ""
        customer.name = stripe_customer["name"] or ""
        customer.shipping = stripe_customer["shipping"]
        customer.tax_exempt = stripe_customer["tax_exempt"]
        customer.preferred_locales = stripe_customer["preferred_locales"]
        customer.invoice_prefix = stripe_customer["invoice_prefix"] or ""
        customer.invoice_settings = stripe_customer["invoice_settings"]
        customer.metadata = stripe_customer["metadata"]
        customer.save()

        return customer

    def sync(self, customer, stripe_customer=None):
        """
        Synchronizes a local Customer object with details from the Stripe API
        Args:
            customer: a Customer object
            stripe_customer: optionally,
            data from the Stripe API representing the customer
        Returns:
            a django_stripe.StripeCustomer object
        """
        if not customer.is_active:
            return

        if not stripe_customer:
            stripe_customer = stripe.Customer.retrieve(customer.stripe_id)

        if stripe_customer.get("deleted", False):
            self.soft_delete(customer)
            return

        # Sync customer details
        customer = self.sync_from_stripe_data(customer, stripe_customer)

        # Django Stripe Stuff
        from django_stripe.actions.payment_methods import StripeCard
        from django_stripe.actions.subscriptions import StripeSubscriptionAction

        # Sync customer card details
        if customer.default_source:
            stripe_source = stripe.Customer.retrieve_source(
                customer.stripe_id, customer.default_source
            )
            StripeCard.sync_from_stripe_data(customer, source=stripe_source)

        # Sync subscription details
        subscriptions = stripe.Subscription.auto_paging_iter(
            customer=customer.stripe_id
        )
        for subscription in subscriptions:
            StripeSubscriptionAction.sync_from_stripe_data(
                customer=customer,
                stripe_subscription=subscription,
            )

        return customer

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