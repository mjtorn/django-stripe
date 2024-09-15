# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Django Stripe Stuff
from django_stripe.actions import StripeProductAction


class StripeProductWebhookTestCase(TestCase):
    def setUp(self):
        # Webhook URL for testing
        self.url = reverse("stripe-webhook-list")

        self.client = APIClient()

        # Base product data used across all events
        self.product_data = {
            "id": "prod_NWjs8kKbJWmuuc",
            "object": "product",
            "active": True,
            "created": 1678833149,
            "default_price": None,
            "description": None,
            "images": [],
            "marketing_features": [],
            "livemode": False,
            "metadata": {},
            "name": "Gold Plan",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "unit_label": None,
            "updated": 1678833149,
            "url": None,
        }

        # Create, delete, update, and trial will end event data
        self.product_created_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "product.created",
            "api_version": "2024-06-20",
            "data": {"object": self.product_data},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

        self.product_deleted_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1726300960,
            "data": {
                "object": self.product_data.copy(),
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
            "type": "product.deleted",
        }

        self.product_updated_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "product.updated",
            "api_version": "2024-06-20",
            "data": {"object": self.product_data.copy()},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

    @patch("stripe.Event.retrieve")
    def test_product_created_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the product_created_data
        mock_stripe_event_retrieve.return_value = self.product_created_data.copy()

        response = self.client.post(
            self.url,
            self.product_created_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

    @patch("stripe.Event.retrieve")
    def test_product_deleted_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the product_deleted_data
        mock_stripe_event_retrieve.return_value = self.product_deleted_data.copy()
        product = StripeProductAction().sync(self.product_data)
        self.assertIsNone(product.date_purged)

        response = self.client.post(
            self.url,
            self.product_deleted_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        product.refresh_from_db()
        self.assertIsNotNone(product.date_purged)

    @patch("stripe.Event.retrieve")
    def test_product_updated_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the product_updated_data
        mock_stripe_event_retrieve.return_value = self.product_updated_data.copy()
        product = StripeProductAction().sync(self.product_data)
        self.product_updated_data["data"]["object"]["description"] = "test description"

        self.assertEqual(product.description, "")
        response = self.client.post(
            self.url,
            self.product_updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        product.refresh_from_db()
        self.assertEqual(product.description, "test description")
