from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django_stripe.models import StripeCustomer


class StripeSubscriptionWebhookTestCase(TestCase):
    def setUp(self):
        # Webhook URL for testing
        self.url = reverse("stripe-webhook-list")

        self.client = APIClient()

        user = User.objects.create_user(
            username="purnendu",
            email="purnendu.kar8@gmail.com",
            password="password",
        )

        # Mock customer data for testing
        self.customer_data = {
            "email": "purnendu.kar8@gmail.com",
            "name": "Purnendu Kar",
            "stripe_id": "cus_QjC48SZoGC5HV5",
            "description": "",  # Description before update
        }

        # Create an existing StripeCustomer object
        # to simulate the current customer in DB
        StripeCustomer.objects.create(
            stripe_id=self.customer_data["stripe_id"],
            email=self.customer_data["email"],
            name=self.customer_data["name"],
            description=self.customer_data["description"],
            user=user,
        )

        # Base subscription data used across all events
        self.subscription_data = {
            "id": "sub_1Prjj6IO5cnPOFxQHnf22SKJ",
            "object": "subscription",
            "application": None,
            "application_fee_percent": None,
            "automatic_tax": {"enabled": False, "liability": None},
            "billing_cycle_anchor": 1724604940,
            "billing_cycle_anchor_config": None,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": False,
            "canceled_at": None,
            "cancellation_details": {
                "comment": None,
                "feedback": None,
                "reason": None,
            },
            "collection_method": "charge_automatically",
            "created": 1724604940,
            "currency": "usd",
            "current_period_end": 1727283340,
            "current_period_start": 1724604940,
            "customer": "cus_QjC48SZoGC5HV5",
            "days_until_due": None,
            "default_payment_method": None,
            "default_source": "card_1PrjirIO5cnPOFxQX13GITTH",
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "ended_at": None,
            "invoice_settings": {
                "account_tax_ids": None,
                "issuer": {"type": "self"},
            },
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_QjC7IdPBDOYEFn",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1724604941,
                        "discounts": [],
                        "metadata": {},
                        "plan": {
                            "id": "price_1PrjhdIO5cnPOFxQqM9IAKzT",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 9900,
                            "amount_decimal": "9900",
                            "billing_scheme": "per_unit",
                            "created": 1724604849,
                            "currency": "usd",
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "meter": None,
                            "nickname": None,
                            "product": "prod_QjC5fuA3ZTkz5U",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed",
                        },
                        "price": {
                            "id": "price_1PrjhdIO5cnPOFxQqM9IAKzT",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1724604849,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_QjC5fuA3ZTkz5U",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "month",
                                "interval_count": 1,
                                "meter": None,
                                "trial_period_days": None,
                                "usage_type": "licensed",
                            },
                            "tax_behavior": "unspecified",
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 9900,
                            "unit_amount_decimal": "9900",
                        },
                        "quantity": 2,
                        "subscription": "sub_1Prjj6IO5cnPOFxQHnf22SKJ",
                        "tax_rates": [],
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": (
                    "/v1/subscription_items?"
                    "subscription=sub_1Prjj6IO5cnPOFxQHnf22SKJ"
                ),
            },
            "latest_invoice": "in_1Prjj6IO5cnPOFxQ1evqMDsR",
            "livemode": False,
            "metadata": {},
            "next_pending_invoice_item_invoice": None,
            "on_behalf_of": None,
            "pause_collection": None,
            "payment_settings": {
                "payment_method_options": None,
                "payment_method_types": None,
                "save_default_payment_method": "off",
            },
            "pending_invoice_item_interval": None,
            "pending_setup_intent": None,
            "pending_update": None,
            "plan": {
                "id": "price_1PrjhdIO5cnPOFxQqM9IAKzT",
                "object": "plan",
                "active": True,
                "aggregate_usage": None,
                "amount": 9900,
                "amount_decimal": "9900",
                "billing_scheme": "per_unit",
                "created": 1724604849,
                "currency": "usd",
                "interval": "month",
                "interval_count": 1,
                "livemode": False,
                "metadata": {},
                "meter": None,
                "nickname": None,
                "product": "prod_QjC5fuA3ZTkz5U",
                "tiers_mode": None,
                "transform_usage": None,
                "trial_period_days": None,
                "usage_type": "licensed",
            },
            "quantity": 2,
            "schedule": None,
            "start_date": 1724604940,
            "status": "active",
            "test_clock": None,
            "transfer_data": None,
            "trial_end": None,
            "trial_settings": {
                "end_behavior": {"missing_payment_method": "create_invoice"}
            },
            "trial_start": None,
        }

        # Create, delete, update, and trial will end event data
        self.subscription_created_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "customer.subscription.created",
            "api_version": "2024-06-20",
            "data": {"object": self.subscription_data},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

        self.subscription_deleted_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1726300960,
            "data": {
                "object": self.subscription_data.copy(),
            },
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
            "type": "customer.subscription.deleted",
        }

        self.subscription_updated_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "customer.subscription.updated",
            "api_version": "2024-06-20",
            "data": {"object": self.subscription_data.copy()},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

        self.subscription_trial_will_end_data = {
            "id": "evt_1PyqwGIO5cnPOFxQNKVNMAsn",
            "object": "event",
            "type": "customer.subscription.trial_will_end",
            "api_version": "2024-06-20",
            "data": {"object": self.subscription_data.copy()},
            "livemode": False,
            "pending_webhooks": 1,
            "request": {
                "id": "req_KWIfN8k8VGpkrk",
                "idempotency_key": "8758c161-3fd7-4045-841b-7628b1812cc8",
            },
        }

    @patch("stripe.Event.retrieve")
    def test_subscription_created_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the subscription_created_data
        mock_stripe_event_retrieve.return_value = self.subscription_created_data.copy()

        response = self.client.post(
            self.url,
            self.subscription_created_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

    @patch("stripe.Event.retrieve")
    def test_subscription_deleted_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the subscription_deleted_data
        mock_stripe_event_retrieve.return_value = self.subscription_deleted_data.copy()

        response = self.client.post(
            self.url,
            self.subscription_deleted_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

    @patch("stripe.Event.retrieve")
    def test_subscription_updated_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the subscription_updated_data
        mock_stripe_event_retrieve.return_value = self.subscription_updated_data.copy()

        response = self.client.post(
            self.url,
            self.subscription_updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

    @patch("stripe.Event.retrieve")
    def test_subscription_trial_will_end_webhook(self, mock_stripe_event_retrieve):
        # Mock Stripe's Event.retrieve to return the subscription_trial_will_end_data
        mock_stripe_event_retrieve.return_value = (
            self.subscription_trial_will_end_data.copy()
        )

        response = self.client.post(
            self.url,
            self.subscription_trial_will_end_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)
