# Third Party Stuff
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase

# Django Stripe Stuff
from django_stripe.actions import StripeCustomerAction
from django_stripe.models import StripeCustomer


class StripeCustomerActionTestCase(TestCase):
    def setUp(self):

        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        # Initialize the StripeCustomerAction with the user
        self.stripe_action = StripeCustomerAction(self.user)

    @patch("stripe.Customer.create")
    def test_create_customer(self, mock_create):
        # Test scenario when customer does not exist and needs to be created
        mock_create.return_value = {
            "id": "cus_NffrFeUfNV2Hib",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1680893993,
            "currency": None,
            "default_source": None,
            "delinquent": False,
            "description": None,
            "discount": None,
            "email": "jennyrosen@example.com",
            "invoice_prefix": "0759376C",
            "invoice_settings": {
                "custom_fields": None,
                "default_payment_method": None,
                "footer": None,
                "rendering_options": None,
            },
            "livemode": False,
            "metadata": {},
            "name": "Jenny Rosen",
            "next_invoice_sequence": 1,
            "phone": None,
            "preferred_locales": [],
            "shipping": None,
            "tax_exempt": "none",
            "test_clock": None,
        }

        customer = self.stripe_action.create(billing_email="testemail@example.com")

        self.assertIsInstance(customer, StripeCustomer)
        self.assertEqual(customer.stripe_id, "cus_NffrFeUfNV2Hib")
        self.assertEqual(customer.user, self.user)

    @patch("stripe.Customer.retrieve")
    def test_get_existing_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Test retrieving the existing customer
        retrieved_customer = self.stripe_action.get()

        self.assertEqual(retrieved_customer, customer)

    @patch("stripe.Customer.retrieve")
    def test_sync_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Mock the Stripe API response
        mock_retrieve.return_value = {
            "id": "cus_test123",
            "balance": 0,
            "currency": "usd",
            "delinquent": False,
            "default_source": None,
            "description": "Test Customer",
            "address": "Test Address",
            "name": "Test Name",
            "shipping": "Test Shipping",
            "tax_exempt": "none",
            "preferred_locales": ["en"],
            "invoice_prefix": "ABC123",
            "invoice_settings": {},
            "metadata": {},
        }

        # Sync the customer data
        synced_customer = self.stripe_action.sync(customer)

        self.assertEqual(synced_customer.balance, 0)
        self.assertEqual(synced_customer.currency, "usd")
        self.assertEqual(synced_customer.name, "Test Name")

    @patch("stripe.Customer.retrieve")
    def test_soft_delete_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Mock the Stripe API response indicating customer is deleted
        mock_retrieve.return_value = {"deleted": True}

        # Sync the customer, which should trigger soft delete
        self.stripe_action.soft_delete(customer.stripe_id)

        # Reload the customer from the database
        customer.refresh_from_db()

        # Check that the customer has been soft deleted
        self.assertIsNotNone(customer.date_purged)

    def test_link_customer(self):
        # Mock the event and customer objects
        event = MagicMock()
        event.kind = "customer.updated"
        event.message = {"data": {"object": {"id": "cus_test123"}}}

        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Link the customer to the event
        linked_event = self.stripe_action.link_customer(event)

        # Check that the customer was linked to the event
        self.assertEqual(linked_event.customer, customer)
