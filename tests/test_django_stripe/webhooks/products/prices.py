# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Django Stripe Stuff
from django_stripe.actions import StripePriceAction, StripeProductAction
from django_stripe.models import StripePrice


class StripePriceWebhookTestCase(TestCase):
    def setUp(self):
        # Webhook URL for testing
        self.url = reverse("stripe-webhook-list")

        self.client = APIClient()

        # Create an existing StripeCustomer object
        # to simulate the current customer in DB
        StripeProductAction().sync(
            {
                "id": "prod_NWjs8kKbJWmuuc",
                "object": "price",
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
        )

        # Base price data used across all events
        self.price_data = {
            "id": "price_1MoBy5LkdIwHu7ixZhnattbh",
            "object": "price",
            "active": True,
            "billing_scheme": "per_unit",
            "created": 1679431181,
            "currency": "usd",
            "custom_unit_amount": None,
            "livemode": False,
            "lookup_key": None,
            "metadata": {},
            "nickname": None,
            "product": "prod_NWjs8kKbJWmuuc",
            "recurring": {
                "aggregate_usage": None,
                "interval": "month",
                "interval_count": 1,
                "trial_period_days": None,
                "usage_type": "licensed",
            },
            "tax_behavior": "unspecified",
            "tiers_mode": None,
            "transform_quantity": None,
            "type": "recurring",
            "unit_amount": 1000,
            "unit_amount_decimal": "1000",
        }

        # Create, delete, update, and trial will end event data
        self.price_created_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "price.created",
            "api_version": "2024-06-20",
            "data": {"object": self.price_data},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

        self.price_deleted_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1726300960,
            "data": {
                "object": self.price_data.copy(),
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
            "type": "price.deleted",
        }

        self.price_updated_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "price.updated",
            "api_version": "2024-06-20",
            "data": {"object": self.price_data.copy()},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

    @patch("stripe.Event.retrieve")
    def test_price_created_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the price_created_data
        mock_stripe_event_retrieve.return_value = self.price_created_data.copy()

        price = StripePrice.objects.filter(stripe_id=self.price_data["id"]).first()
        self.assertIsNone(price)

        response = self.client.post(
            self.url,
            self.price_created_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

        price = StripePrice.objects.filter(stripe_id=self.price_data["id"]).first()
        self.assertIsNotNone(price)

    @patch("stripe.Event.retrieve")
    def test_price_deleted_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the price_deleted_data
        mock_stripe_event_retrieve.return_value = self.price_deleted_data.copy()
        price = StripePriceAction().sync(self.price_data)
        self.assertIsNone(price.deleted_at)

        response = self.client.post(
            self.url,
            self.price_deleted_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        price.refresh_from_db()
        self.assertIsNotNone(price.deleted_at)

    @patch("stripe.Event.retrieve")
    def test_price_updated_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the price_updated_data
        mock_stripe_event_retrieve.return_value = self.price_updated_data.copy()
        price = StripePriceAction().sync(self.price_data)
        self.price_updated_data["data"]["object"]["unit_amount"] = 2000

        self.assertEqual(price.unit_amount, 1000)
        response = self.client.post(
            self.url,
            self.price_updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        price.refresh_from_db()
        self.assertEqual(price.unit_amount, 2000)
