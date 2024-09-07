# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
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

        self.stripe_customer_data = {
            "id": "cus_NffrFeUfNV2Hib",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1680893993,
            "currency": "usd",
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

    @patch("stripe.Customer.create")
    def test_create_customer(self, mock_create):
        # Test scenario when customer does not exist and needs to be created
        mock_create.return_value = self.stripe_customer_data

        customer = self.stripe_action.create(billing_email="testemail@example.com")

        self.assertEqual(customer.balance, self.stripe_customer_data["balance"])
        self.assertEqual(customer.currency, self.stripe_customer_data["currency"])
        self.assertEqual(customer.name, self.stripe_customer_data["name"])
        self.assertEqual(customer.address, self.stripe_customer_data["address"] or "")
        self.assertEqual(
            customer.default_source,
            self.stripe_customer_data["default_source"] or "",
        )
        self.assertEqual(
            customer.description, self.stripe_customer_data["description"] or ""
        )
        # self.assertEqual(
        #     customer.discount, self.stripe_customer_data["discount"] or ""
        # )
        # self.assertEqual(
        #     customer.phone, self.stripe_customer_data["phone"] or ""
        # )
        self.assertEqual(customer.shipping, self.stripe_customer_data["shipping"])

        # Other fields
        self.assertEqual(
            customer.invoice_prefix, self.stripe_customer_data["invoice_prefix"]
        )
        self.assertEqual(customer.delinquent, self.stripe_customer_data["delinquent"])
        self.assertEqual(
            customer.invoice_settings,
            self.stripe_customer_data["invoice_settings"],
        )
        self.assertEqual(customer.livemode, self.stripe_customer_data["livemode"])
        self.assertEqual(customer.metadata, self.stripe_customer_data["metadata"])
        # self.assertEqual(
        #     customer.next_invoice_sequence,
        #     self.stripe_customer_data["next_invoice_sequence"],
        # )
        self.assertEqual(
            customer.preferred_locales,
            self.stripe_customer_data["preferred_locales"],
        )
        self.assertEqual(customer.tax_exempt, self.stripe_customer_data["tax_exempt"])
        # self.assertEqual(
        #     customer.test_clock, self.stripe_customer_data["test_clock"]
        # )

    @patch("stripe.Customer.retrieve")
    def test_get_existing_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Test retrieving the existing customer
        retrieved_customer = self.stripe_action.get()

        # Assert all fields for existing customer
        self.assertEqual(retrieved_customer, customer)
        self.assertEqual(retrieved_customer.stripe_id, "cus_test123")
        self.assertEqual(retrieved_customer.user, self.user)
        self.assertTrue(retrieved_customer.is_active)

    @patch("stripe.Customer.retrieve")
    def test_sync_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Mock the Stripe API response
        mock_retrieve.return_value = self.stripe_customer_data

        # Sync the customer data
        synced_customer = self.stripe_action.sync(customer)

        self.assertEqual(synced_customer.balance, self.stripe_customer_data["balance"])
        self.assertEqual(
            synced_customer.currency, self.stripe_customer_data["currency"]
        )
        self.assertEqual(synced_customer.name, self.stripe_customer_data["name"])
        self.assertEqual(
            synced_customer.address, self.stripe_customer_data["address"] or ""
        )
        self.assertEqual(
            synced_customer.default_source,
            self.stripe_customer_data["default_source"] or "",
        )
        self.assertEqual(
            synced_customer.description, self.stripe_customer_data["description"] or ""
        )
        # self.assertEqual(
        #     synced_customer.discount, self.stripe_customer_data["discount"] or ""
        # )
        # self.assertEqual(
        #     synced_customer.phone, self.stripe_customer_data["phone"] or ""
        # )
        self.assertEqual(
            synced_customer.shipping, self.stripe_customer_data["shipping"]
        )

        # Other fields
        self.assertEqual(
            synced_customer.invoice_prefix, self.stripe_customer_data["invoice_prefix"]
        )
        self.assertEqual(
            synced_customer.delinquent, self.stripe_customer_data["delinquent"]
        )
        self.assertEqual(
            synced_customer.invoice_settings,
            self.stripe_customer_data["invoice_settings"],
        )
        self.assertEqual(
            synced_customer.livemode, self.stripe_customer_data["livemode"]
        )
        self.assertEqual(
            synced_customer.metadata, self.stripe_customer_data["metadata"]
        )
        # self.assertEqual(
        #     synced_customer.next_invoice_sequence,
        #     self.stripe_customer_data["next_invoice_sequence"],
        # )
        self.assertEqual(
            synced_customer.preferred_locales,
            self.stripe_customer_data["preferred_locales"],
        )
        self.assertEqual(
            synced_customer.tax_exempt, self.stripe_customer_data["tax_exempt"]
        )
        # self.assertEqual(
        #     synced_customer.test_clock, self.stripe_customer_data["test_clock"]
        # )

    @patch("stripe.Customer.retrieve")
    def test_soft_delete_customer(self, mock_retrieve):
        # Create a customer in the database
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_id="cus_test123", is_active=True
        )

        # Mock the Stripe API response indicating customer is deleted
        mock_retrieve.return_value = {"deleted": True}

        self.assertIsNone(customer.date_purged)

        # Sync the customer, which should trigger soft delete
        self.stripe_action.soft_delete(customer.stripe_id)

        # Reload the customer from the database
        customer.refresh_from_db()

        # Assert that the customer has been soft deleted
        self.assertIsNotNone(customer.date_purged)
