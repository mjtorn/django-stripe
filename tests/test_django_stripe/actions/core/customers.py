# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.apps import apps
from django.conf import settings
from django.test import TestCase

# Django Stripe Stuff
from django_stripe.actions import StripeCustomerAction
from django_stripe.models import StripeCustomer


class StripeCustomerActionTest(TestCase):
    def setUp(self):
        self.action = StripeCustomerAction()
        self.stripe_data = {
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
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        self.user = user_model.objects.create(
            email=self.stripe_data["email"], username="jenny"
        )

    def test_sync(self):
        # Mocking the stripe customer data
        stripe_data = self.stripe_data.copy()

        # Execute sync method
        self.action.sync(stripe_data)

        # Assertions
        customer = StripeCustomer.objects.get(stripe_id=self.stripe_data["id"])
        self.assertEqual(customer.email, self.stripe_data["email"])
        self.assertEqual(customer.name, self.stripe_data["name"])
        self.assertEqual(customer.user, self.user)

    @patch("stripe.Customer.retrieve")
    def test_sync_by_ids(self, mock_retrieve):
        # Mocking the stripe customer data
        stripe_data = self.stripe_data.copy()
        mock_retrieve.return_value = stripe_data

        # Execute sync_by_ids method
        self.action.sync_by_ids([stripe_data["id"]])

        # Assertions
        customer = StripeCustomer.objects.get(stripe_id=self.stripe_data["id"])
        self.assertEqual(customer.email, self.stripe_data["email"])
        self.assertEqual(customer.name, self.stripe_data["name"])
        self.assertEqual(customer.user, self.user)

    @patch("stripe.Customer.auto_paging_iter")
    def test_sync_all(self, mock_auto_paging_iter):
        # Mocking the stripe customers data
        stripe_customers = [
            {
                "id": "cus_test1",
                "object": "customer",
                "created": 1678037688,
                "email": "test1@example.com",
                "metadata": {},
                "name": "Customer One",
                "source": None,
            },
            {
                "id": "cus_test2",
                "object": "customer",
                "created": 1678037689,
                "email": "test2@example.com",
                "metadata": {},
                "name": "Customer Two",
                "source": None,
            },
            self.stripe_data.copy(),
        ]
        mock_auto_paging_iter.return_value = stripe_customers

        # Clear existing customers
        StripeCustomer.objects.all().delete()

        # Execute sync_all method
        self.action.sync_all()

        # Assertions
        customers = StripeCustomer.objects.all()
        self.assertEqual(customers.count(), 3)

        customer = StripeCustomer.objects.get(stripe_id=self.stripe_data["id"])
        self.assertEqual(customer.email, self.stripe_data["email"])
        self.assertEqual(customer.name, self.stripe_data["name"])
        self.assertEqual(customer.user, self.user)

    @patch("stripe.Customer.auto_paging_iter")
    def test_sync_all_with_deleted_objects(self, mock_auto_paging_iter):
        # Mocking the stripe customers data
        stripe_customers = [
            {
                "id": "cus_test1",
                "object": "customer",
                "created": 1678037688,
                "email": "test1@example.com",
                "metadata": {},
                "name": "Customer One",
                "source": None,
            }
        ]
        mock_auto_paging_iter.return_value = stripe_customers

        # Create a customer that will be deleted
        StripeCustomer.objects.create(
            stripe_id="cus_test2",
            email="test2@example.com",
            name="Customer Two",
        )

        # Execute sync_all method
        self.action.sync_all()

        # Assertions
        customers = StripeCustomer.objects.filter(date_purged__isnull=False)
        self.assertEqual(customers.count(), 1)
        self.assertTrue(
            StripeCustomer.objects.filter(
                stripe_id="cus_test2", date_purged__isnull=False
            ).exists()
        )

    @patch("stripe.Customer.auto_paging_iter")
    def test_sync_batch(self, mock_auto_paging_iter):
        # Mocking the stripe customers data
        stripe_customers = [
            {
                "id": "cus_test1",
                "object": "customer",
                "created": 1678037688,
                "email": "test1@example.com",
                "metadata": {},
                "name": "Customer One",
                "source": None,
            }
        ]
        mock_auto_paging_iter.return_value = stripe_customers

        # Execute sync_batch method
        self.action.sync_batch(stripe_customers)

        # Assertions
        customer = StripeCustomer.objects.get(stripe_id="cus_test1")
        self.assertEqual(customer.email, "test1@example.com")
        self.assertEqual(customer.name, "Customer One")
        self.assertEqual(customer.user, None)

    def test_soft_delete(self):
        # Create a customer that will be soft-deleted
        customer = StripeCustomer.objects.create(
            stripe_id="cus_test",
            email="test@example.com",
            name="Test Customer",
        )

        # Execute soft_delete method
        self.action.soft_delete("cus_test")

        # Assertions
        customer.refresh_from_db()
        self.assertIsNotNone(customer.date_purged)
