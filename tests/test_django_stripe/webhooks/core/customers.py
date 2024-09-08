# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# Django Stripe Stuff
from django_stripe.models import StripeCustomer


class CustomerUpdatedWebhookTestCase(TestCase):
    def setUp(self):
        # Setup the API client
        self.client = APIClient()

        # Mock customer data for testing (before the update)
        self.customer_data_before = {
            "email": "purnendu.kar8@gmail.com",
            "name": "Purnendu Kar",
            "stripe_id": "cus_QjC48SZoGC5HV5",
            "description": "",  # Description before update
        }

        # Create an existing StripeCustomer object
        # to simulate the current customer in DB
        self.customer = StripeCustomer.objects.create(
            stripe_id=self.customer_data_before["stripe_id"],
            email=self.customer_data_before["email"],
            name=self.customer_data_before["name"],
            description=self.customer_data_before["description"],
        )

        # Mock event data from Stripe for testing (customer.updated)
        self.event_data = {
            "id": "evt_1PwPfEIO5cnPOFxQkKhmOfj9",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1725719460,
            "data": {
                "object": {
                    "id": "cus_QjC48SZoGC5HV5",
                    "object": "customer",
                    "address": None,
                    "balance": 0,
                    "created": 1724604770,
                    "currency": "usd",
                    "default_source": "card_1PrjirIO5cnPOFxQX13GITTH",
                    "delinquent": False,
                    "description": "just desc",  # Updated description
                    "discount": None,
                    "email": "purnendu.kar8@gmail.com",
                    "invoice_prefix": "0A66AED6",
                    "invoice_settings": {
                        "custom_fields": None,
                        "default_payment_method": None,
                        "footer": None,
                        "rendering_options": None,
                    },
                    "livemode": False,
                    "metadata": {},
                    "name": "Purnendu Kar",
                    "next_invoice_sequence": 2,
                    "phone": "+918334035754",
                    "preferred_locales": [],
                    "shipping": {
                        "address": {
                            "city": "",
                            "country": "",
                            "line1": "",
                            "line2": "",
                            "postal_code": "",
                            "state": "",
                        },
                        "name": "Purnendu Kar",
                        "phone": "+918334035754",
                    },
                    "tax_exempt": "none",
                    "test_clock": None,
                },
                "previous_attributes": {
                    "description": None  # Description was previously None
                },
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_IskUPKAZ7ilcLq",
                "idempotency_key": "3a8024d0-6a1d-4cca-a891-03ce9ceab2df",
            },
            "type": "customer.updated",
        }

    @patch("stripe.Event.retrieve")
    def test_customer_updated_webhook(self, mock_event):
        mock_event.return_value = self.event_data.copy()

        # Simulate the webhook POST request for customer.updated
        response = self.client.post(
            reverse("stripe-webhook-list"), self.event_data, format="json"
        )

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the customer in the database has been updated
        updated_customer = StripeCustomer.objects.get(
            stripe_id=self.customer_data_before["stripe_id"]
        )
        self.assertEqual(
            updated_customer.description,
            self.event_data["data"]["object"]["description"],
        )  # Updated description


class CustomerCreatedWebhookTestCase(TestCase):
    def setUp(self):
        # Setup the API client
        self.client = APIClient()

        User.objects.create(email="purnendu.kar8@gmail.com")

        # Mock event data from Stripe for testing (customer.updated)
        self.event_data = {
            "id": "evt_1PwPfEIO5cnPOFxQkKhmOfj9",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1725719460,
            "data": {
                "object": {
                    "id": "cus_QjC48SZoGC5HV5",
                    "object": "customer",
                    "address": None,
                    "balance": 0,
                    "created": 1724604770,
                    "currency": "usd",
                    "default_source": "card_1PrjirIO5cnPOFxQX13GITTH",
                    "delinquent": False,
                    "description": "just desc",  # Updated description
                    "discount": None,
                    "email": "purnendu.kar8@gmail.com",
                    "invoice_prefix": "0A66AED6",
                    "invoice_settings": {
                        "custom_fields": None,
                        "default_payment_method": None,
                        "footer": None,
                        "rendering_options": None,
                    },
                    "livemode": False,
                    "metadata": {},
                    "name": "Purnendu Kar",
                    "next_invoice_sequence": 2,
                    "phone": "+918334035754",
                    "preferred_locales": [],
                    "shipping": {
                        "address": {
                            "city": "",
                            "country": "",
                            "line1": "",
                            "line2": "",
                            "postal_code": "",
                            "state": "",
                        },
                        "name": "Purnendu Kar",
                        "phone": "+918334035754",
                    },
                    "tax_exempt": "none",
                    "test_clock": None,
                },
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_IskUPKAZ7ilcLq",
                "idempotency_key": "3a8024d0-6a1d-4cca-a891-03ce9ceab2df",
            },
            "type": "customer.created",
        }

    @patch("stripe.Event.retrieve")
    def test_customer_created_webhook(self, mock_event):
        mock_event.return_value = self.event_data.copy()
        # Simulate the webhook POST request for customer.updated
        response = self.client.post(
            reverse("stripe-webhook-list"), self.event_data, format="json"
        )

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the customer in the database has been updated
        updated_customer = StripeCustomer.objects.filter(
            stripe_id=self.event_data["data"]["object"]["id"]
        ).first()
        self.assertIsNotNone(updated_customer)


class CustomerDeletedWebhookTestCase(TestCase):
    def setUp(self):
        # Setup the API client
        self.client = APIClient()

        user = User.objects.create(email="purnendu.kar8@gmail.com")
        self.customer_data_before = {
            "email": "purnendu.kar8@gmail.com",
            "name": "Purnendu Kar",
            "stripe_id": "cus_QjC48SZoGC5HV5",
            "description": "",  # Description before update
        }

        # Create an existing StripeCustomer object
        # to simulate the current customer in DB
        self.customer = StripeCustomer.objects.create(
            stripe_id=self.customer_data_before["stripe_id"],
            email=self.customer_data_before["email"],
            name=self.customer_data_before["name"],
            description=self.customer_data_before["description"],
            user=user,
        )

        # Mock event data from Stripe for testing (customer.updated)
        self.event_data = {
            "id": "evt_1PwPfEIO5cnPOFxQkKhmOfj9",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1725719460,
            "data": {
                "object": {
                    "id": "cus_QjC48SZoGC5HV5",
                    "object": "customer",
                    "address": None,
                    "balance": 0,
                    "created": 1724604770,
                    "currency": "usd",
                    "default_source": "card_1PrjirIO5cnPOFxQX13GITTH",
                    "delinquent": False,
                    "description": "just desc",  # Updated description
                    "discount": None,
                    "email": "purnendu.kar8@gmail.com",
                    "invoice_prefix": "0A66AED6",
                    "invoice_settings": {
                        "custom_fields": None,
                        "default_payment_method": None,
                        "footer": None,
                        "rendering_options": None,
                    },
                    "livemode": False,
                    "metadata": {},
                    "name": "Purnendu Kar",
                    "next_invoice_sequence": 2,
                    "phone": "+918334035754",
                    "preferred_locales": [],
                    "shipping": {
                        "address": {
                            "city": "",
                            "country": "",
                            "line1": "",
                            "line2": "",
                            "postal_code": "",
                            "state": "",
                        },
                        "name": "Purnendu Kar",
                        "phone": "+918334035754",
                    },
                    "tax_exempt": "none",
                    "test_clock": None,
                },
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_IskUPKAZ7ilcLq",
                "idempotency_key": "3a8024d0-6a1d-4cca-a891-03ce9ceab2df",
            },
            "type": "customer.deleted",
        }

    @patch("stripe.Event.retrieve")
    def test_customer_deleted_webhook(self, mock_event):
        mock_event.return_value = self.event_data.copy()
        # Simulate the webhook POST request for customer.updated
        response = self.client.post(
            reverse("stripe-webhook-list"), self.event_data, format="json"
        )

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the customer in the database has been updated
        updated_customer = StripeCustomer.objects.filter(
            stripe_id=self.event_data["data"]["object"]["id"]
        ).first()
        self.assertIsNotNone(updated_customer)
