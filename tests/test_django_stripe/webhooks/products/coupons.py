# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Django Stripe Stuff
from django_stripe.actions import StripeCouponAction
from django_stripe.models import StripeCoupon


class StripeCouponWebhookTestCase(TestCase):
    def setUp(self):
        # Webhook URL for testing
        self.url = reverse("stripe-webhook-list")

        self.client = APIClient()

        # Base coupon data used across all events
        self.coupon_data = {
            "id": "jMT0WJUD",
            "object": "coupon",
            "amount_off": None,
            "created": 1678037688,
            "currency": None,
            "duration": "repeating",
            "duration_in_months": 3,
            "livemode": False,
            "max_redemptions": None,
            "metadata": {},
            "name": None,
            "percent_off": 25.5,
            "redeem_by": None,
            "times_redeemed": 0,
            "valid": True,
        }

        # Create, delete, update, and trial will end event data
        self.coupon_created_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "coupon.created",
            "api_version": "2024-06-20",
            "data": {"object": self.coupon_data},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

        self.coupon_deleted_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1726300960,
            "data": {
                "object": self.coupon_data.copy(),
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
            "type": "coupon.deleted",
        }

        self.coupon_updated_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "coupon.updated",
            "api_version": "2024-06-20",
            "data": {"object": self.coupon_data.copy()},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

    @patch("stripe.Event.retrieve")
    def test_coupon_created_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the coupon_created_data
        mock_stripe_event_retrieve.return_value = self.coupon_created_data.copy()

        coupon = StripeCoupon.objects.filter(stripe_id=self.coupon_data["id"]).first()
        self.assertIsNone(coupon)

        response = self.client.post(
            self.url,
            self.coupon_created_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

        coupon = StripeCoupon.objects.filter(stripe_id=self.coupon_data["id"]).first()
        self.assertIsNotNone(coupon)

    @patch("stripe.Event.retrieve")
    def test_coupon_deleted_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the coupon_deleted_data
        mock_stripe_event_retrieve.return_value = self.coupon_deleted_data.copy()
        coupon = StripeCouponAction().sync(self.coupon_data)
        self.assertIsNone(coupon.deleted_at)

        response = self.client.post(
            self.url,
            self.coupon_deleted_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        coupon.refresh_from_db()
        self.assertIsNotNone(coupon.deleted_at)

    @patch("stripe.Event.retrieve")
    def test_coupon_updated_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the coupon_updated_data
        mock_stripe_event_retrieve.return_value = self.coupon_updated_data.copy()
        coupon = StripeCouponAction().sync(self.coupon_data)
        self.coupon_updated_data["data"]["object"]["name"] = "dummy"

        self.assertEqual(coupon.name, "")
        response = self.client.post(
            self.url,
            self.coupon_updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
        coupon.refresh_from_db()
        self.assertEqual(coupon.name, "dummy")
