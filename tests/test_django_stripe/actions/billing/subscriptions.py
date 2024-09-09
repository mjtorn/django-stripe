from unittest.mock import patch

from django.test import TestCase

from django_stripe.actions import StripeSubscriptionAction
from django_stripe.models import StripeCustomer, StripeSubscription


class StripeSubscriptionActionTestCase(TestCase):
    def setUp(self):
        # Setup initial data
        self.stripe_customer = StripeCustomer.objects.create(
            stripe_id="cus_Na6dX7aXxi11N4", email="customer@example.com"
        )

        self.subscription_data = {
            "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
            "object": "subscription",
            "application": None,
            "application_fee_percent": None,
            "automatic_tax": {"enabled": False, "liability": None},
            "billing_cycle_anchor": 1679609767,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": False,
            "canceled_at": None,
            "cancellation_details": {"comment": None, "feedback": None, "reason": None},
            "collection_method": "charge_automatically",
            "created": 1679609767,
            "currency": "usd",
            "current_period_end": 1682288167,
            "current_period_start": 1679609767,
            "customer": "cus_Na6dX7aXxi11N4",
            "days_until_due": None,
            "default_payment_method": None,
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": None,
            "ended_at": None,
            "invoice_settings": {"issuer": {"type": "self"}},
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_Na6dzxczY5fwHx",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1679609768,
                        "metadata": {},
                        "plan": {
                            "id": "price_1MowQULkdIwHu7ixraBm864M",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 1000,
                            "amount_decimal": "1000",
                            "billing_scheme": "per_unit",
                            "created": 1679609766,
                            "currency": "usd",
                            "discounts": None,
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_Na6dGcTsmU0I4R",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed",
                        },
                        "price": {
                            "id": "price_1MowQULkdIwHu7ixraBm864M",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1679609766,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_Na6dGcTsmU0I4R",
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
                        },
                        "quantity": 1,
                        "subscription": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
                        "tax_rates": [],
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": (
                    "/v1/subscription_items?"
                    "subscription=sub_1MowQVLkdIwHu7ixeRlqHVzs"
                ),
            },
            "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",
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
            "schedule": None,
            "start_date": 1679609767,
            "status": "active",
            "test_clock": None,
            "transfer_data": None,
            "trial_end": None,
            "trial_settings": {
                "end_behavior": {"missing_payment_method": "create_invoice"}
            },
            "trial_start": None,
        }

    @patch("stripe.Subscription.retrieve")
    def test_sync_creates_subscription(self, mock_retrieve):
        # Mock the Stripe API call
        mock_retrieve.return_value = self.subscription_data.copy()

        action = StripeSubscriptionAction(
            stripe_customer_id=self.stripe_customer.stripe_id
        )
        action.sync(self.subscription_data.copy())

        # Test if the subscription was created in the database
        subscription = StripeSubscription.objects.get(
            stripe_id="sub_1MowQVLkdIwHu7ixeRlqHVzs"
        )

        # Handle None values by using `or ""` or an appropriate default
        self.assertEqual(subscription.currency, self.subscription_data["currency"])
        self.assertEqual(subscription.status, self.subscription_data["status"])
        # self.assertEqual(
        #     subscription.description, self.subscription_data["description"]
        # )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        # self.assertEqual(
        #     subscription.application, self.subscription_data["application"]
        # )
        # self.assertEqual(
        #     subscription.application_fee_percent,
        #     self.subscription_data["application_fee_percent"],
        # )
        self.assertEqual(
            subscription.billing_thresholds,
            self.subscription_data["billing_thresholds"],
        )
        self.assertEqual(subscription.cancel_at, self.subscription_data["cancel_at"])
        self.assertEqual(
            subscription.canceled_at, self.subscription_data["canceled_at"]
        )
        self.assertEqual(
            subscription.default_payment_method,
            self.subscription_data["default_payment_method"] or "",
        )
        self.assertEqual(
            subscription.default_source, self.subscription_data["default_source"] or ""
        )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        self.assertEqual(subscription.ended_at, self.subscription_data["ended_at"])
        self.assertEqual(
            subscription.days_until_due, self.subscription_data["days_until_due"]
        )
        self.assertEqual(
            subscription.next_pending_invoice_item_invoice,
            self.subscription_data["next_pending_invoice_item_invoice"],
        )
        # self.assertEqual(
        #     subscription.on_behalf_of, self.subscription_data["on_behalf_of"]
        # )
        self.assertEqual(
            subscription.pause_collection,
            self.subscription_data["pause_collection"],
        )
        self.assertEqual(
            subscription.pending_invoice_item_interval,
            self.subscription_data["pending_invoice_item_interval"],
        )
        self.assertEqual(
            subscription.pending_setup_intent,
            self.subscription_data["pending_setup_intent"] or "",
        )
        self.assertEqual(
            subscription.pending_update, self.subscription_data["pending_update"]
        )
        # self.assertEqual(subscription.schedule, self.subscription_data["schedule"])
        self.assertEqual(subscription.trial_end, self.subscription_data["trial_end"])
        self.assertEqual(
            subscription.trial_start, self.subscription_data["trial_start"]
        )
        # self.assertEqual(
        #   subscription.test_clock,
        #   self.subscription_data["test_clock"]
        # )
        # self.assertEqual(
        #     subscription.transfer_data, self.subscription_data["transfer_data"]
        # )
        self.assertEqual(
            subscription.metadata, self.subscription_data["metadata"] or {}
        )

    @patch("stripe.Subscription.retrieve")
    def test_sync_updates_subscription(self, mock_retrieve):
        # Create an existing subscription in the database
        subscription_data = self.subscription_data.copy()
        subscription_data["status"] = "inactive"

        # Mock the Stripe API call
        mock_retrieve.return_value = self.subscription_data.copy()

        action = StripeSubscriptionAction(
            stripe_customer_id=self.stripe_customer.stripe_id
        )
        existing_subscription = action.sync(subscription_data.copy())

        # Update existing data
        action.sync(self.subscription_data.copy())

        # Test if the subscription was updated
        existing_subscription.refresh_from_db()
        self.assertEqual(existing_subscription.status, "active")

    @patch("stripe.Subscription.retrieve")
    def test_sync_batch(self, mock_retrieve):
        # Mock the Stripe API call
        mock_retrieve.return_value = self.subscription_data.copy()

        action = StripeSubscriptionAction(
            stripe_customer_id=self.stripe_customer.stripe_id
        )
        action.sync_batch([self.subscription_data.copy()])

        # Test if the subscription was created in the database
        subscription = StripeSubscription.objects.get(
            stripe_id="sub_1MowQVLkdIwHu7ixeRlqHVzs"
        )

        # Handle None values by using `or ""` or an appropriate default
        self.assertEqual(subscription.currency, self.subscription_data["currency"])
        self.assertEqual(subscription.status, self.subscription_data["status"])
        # self.assertEqual(
        #     subscription.description, self.subscription_data["description"]
        # )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        # self.assertEqual(
        #     subscription.application, self.subscription_data["application"]
        # )
        # self.assertEqual(
        #     subscription.application_fee_percent,
        #     self.subscription_data["application_fee_percent"],
        # )
        self.assertEqual(
            subscription.billing_thresholds,
            self.subscription_data["billing_thresholds"],
        )
        self.assertEqual(subscription.cancel_at, self.subscription_data["cancel_at"])
        self.assertEqual(
            subscription.canceled_at, self.subscription_data["canceled_at"]
        )
        self.assertEqual(
            subscription.default_payment_method,
            self.subscription_data["default_payment_method"] or "",
        )
        self.assertEqual(
            subscription.default_source, self.subscription_data["default_source"] or ""
        )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        self.assertEqual(subscription.ended_at, self.subscription_data["ended_at"])
        self.assertEqual(
            subscription.days_until_due, self.subscription_data["days_until_due"]
        )
        self.assertEqual(
            subscription.next_pending_invoice_item_invoice,
            self.subscription_data["next_pending_invoice_item_invoice"],
        )
        # self.assertEqual(
        #     subscription.on_behalf_of, self.subscription_data["on_behalf_of"]
        # )
        self.assertEqual(
            subscription.pause_collection,
            self.subscription_data["pause_collection"],
        )
        self.assertEqual(
            subscription.pending_invoice_item_interval,
            self.subscription_data["pending_invoice_item_interval"],
        )
        self.assertEqual(
            subscription.pending_setup_intent,
            self.subscription_data["pending_setup_intent"] or "",
        )
        self.assertEqual(
            subscription.pending_update, self.subscription_data["pending_update"]
        )
        # self.assertEqual(subscription.schedule, self.subscription_data["schedule"])
        self.assertEqual(subscription.trial_end, self.subscription_data["trial_end"])
        self.assertEqual(
            subscription.trial_start, self.subscription_data["trial_start"]
        )
        # self.assertEqual(
        #   subscription.test_clock,
        #   self.subscription_data["test_clock"]
        # )
        # self.assertEqual(
        #     subscription.transfer_data, self.subscription_data["transfer_data"]
        # )
        self.assertEqual(
            subscription.metadata, self.subscription_data["metadata"] or {}
        )

    @patch("stripe.Subscription.auto_paging_iter")
    def test_sync_all(self, mock_auto_paging_iter):
        # Mock the Stripe API call
        mock_auto_paging_iter.return_value = [self.subscription_data.copy()]

        action = StripeSubscriptionAction(
            stripe_customer_id=self.stripe_customer.stripe_id
        )
        action.sync_all()

        # Test if the subscription was created in the database
        subscription = StripeSubscription.objects.get(
            stripe_id="sub_1MowQVLkdIwHu7ixeRlqHVzs"
        )

        # Handle None values by using `or ""` or an appropriate default
        self.assertEqual(subscription.currency, self.subscription_data["currency"])
        self.assertEqual(subscription.status, self.subscription_data["status"])
        # self.assertEqual(
        #     subscription.description, self.subscription_data["description"]
        # )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        # self.assertEqual(
        #     subscription.application, self.subscription_data["application"]
        # )
        # self.assertEqual(
        #     subscription.application_fee_percent,
        #     self.subscription_data["application_fee_percent"],
        # )
        self.assertEqual(
            subscription.billing_thresholds,
            self.subscription_data["billing_thresholds"],
        )
        self.assertEqual(subscription.cancel_at, self.subscription_data["cancel_at"])
        self.assertEqual(
            subscription.canceled_at, self.subscription_data["canceled_at"]
        )
        self.assertEqual(
            subscription.default_payment_method,
            self.subscription_data["default_payment_method"] or "",
        )
        self.assertEqual(
            subscription.default_source, self.subscription_data["default_source"] or ""
        )
        # self.assertEqual(
        #     subscription.discount, self.subscription_data["discount"]
        # )
        self.assertEqual(subscription.ended_at, self.subscription_data["ended_at"])
        self.assertEqual(
            subscription.days_until_due, self.subscription_data["days_until_due"]
        )
        self.assertEqual(
            subscription.next_pending_invoice_item_invoice,
            self.subscription_data["next_pending_invoice_item_invoice"],
        )
        # self.assertEqual(
        #     subscription.on_behalf_of, self.subscription_data["on_behalf_of"]
        # )
        self.assertEqual(
            subscription.pause_collection,
            self.subscription_data["pause_collection"],
        )
        self.assertEqual(
            subscription.pending_invoice_item_interval,
            self.subscription_data["pending_invoice_item_interval"],
        )
        self.assertEqual(
            subscription.pending_setup_intent,
            self.subscription_data["pending_setup_intent"] or "",
        )
        self.assertEqual(
            subscription.pending_update, self.subscription_data["pending_update"]
        )
        # self.assertEqual(subscription.schedule, self.subscription_data["schedule"])
        self.assertEqual(subscription.trial_end, self.subscription_data["trial_end"])
        self.assertEqual(
            subscription.trial_start, self.subscription_data["trial_start"]
        )
        # self.assertEqual(
        #   subscription.test_clock,
        #   self.subscription_data["test_clock"]
        # )
        # self.assertEqual(
        #     subscription.transfer_data, self.subscription_data["transfer_data"]
        # )
        self.assertEqual(
            subscription.metadata, self.subscription_data["metadata"] or {}
        )
