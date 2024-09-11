Stripe Subscription
=====================

The `StripeSubscriptionAction` class is a part of the Django Stripe library, which provides a set of actions for synchronizing local Stripe subscription data with the Stripe API. This class is designed to handle the complexities of retrieving and updating subscription data, making it easier to integrate Stripe with your Django application.

The `StripeSubscriptionAction` class is defined in the `django_stripe.actions` module and has the following key characteristics:

*   **Model Class**: The `StripeSubscriptionAction` class is associated with the `StripeSubscription` model.
*   **Stripe Object Class**: The class uses the `stripe.Subscription` object to interact with the Stripe API.
*   **Syncing Method**: The class provides a `sync_all` method to synchronize all local Stripe subscription data with the Stripe API.

Overall, the `StripeSubscriptionAction` class provides a convenient and efficient way to manage Stripe subscription data in your Django application.

## Methods

### Sync All Subscriptions

**Method:** `sync_all(self)`

This method is used to synchronize all local Stripe subscriptions data with the Stripe API. It retrieves a batch of subscriptions from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync all subscriptions"
    ```python
    from django_stripe.actions import StripeSubscriptionAction

    stripe_action = StripeSubscriptionAction()
    stripe_action.sync_all()
    ```

In this example, the `sync_all` method is called to synchronize all local Stripe customer data with the Stripe API.

### Sync Subscriptions for given IDs

**Method:** `sync_by_ids(self, ids: list)`

This method is used to synchronize local Stripe customer data for a specific list of customer IDs. It retrieves the subscriptions from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync Subscriptions for given IDs"
    ```python
    from django_stripe.actions import StripeSubscriptionAction

    stripe_action = StripeSubscriptionAction()
    ids = ['sub_1MowQVLkdIwHu7ixeRlqHVzs', 'sub_1MowQVLkdIwHu7ixeRlqHVzw']
    stripe_action.sync_by_ids(ids)
    ```

In this example, the `sync_by_ids` method is called with a list of customer IDs to synchronize.

### Sync Batch of Subscriptions

**Methods:** `sync_batch(self, batch:list[dict])`

This method is used to synchronize a batch of local Stripe customer data. It takes a list of customer data as an argument and iterates over it, calling the `sync` method on each one.

!!! Example "Sync Batch of Subscriptions"
    ```python
    from django_stripe.actions import StripeSubscriptionAction

    stripe_action = StripeSubscriptionAction()
    batch = [
        {
            "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",
            "object": "subscription",
            "application_fee_percent": None,
            "billing_cycle_anchor": 1643715200,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": None,
            "canceled_at": None,
            "collection_method": "charge_automatically",
            "created": 1643715200,
            "currency": "usd",
            "current_period_end": 1646307200,
            "current_period_start": 1643715200,
            "customer": "cus_NhD8HD2bY8dP3V",
            "days_until_due": None,
            "default_payment_method": None,
            "default_source": None,
            "default_tax_rates": None,
            "discount": None,
            "ended_at": None,
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_NhD8HD2bY8dP3V",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1643715200,
                        "metadata": {},
                        "plan": {
                            "id": "price_1MowQVLkdIwHu7ixeRlqHVzb",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "currency": "usd",
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_NhD8HD2bY8dP3V",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "month",
                                "interval_count": 1,
                                "usage_type": "licensed"
                            },
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 1000,
                            "unit_amount_decimal": "1000"
                        },
                        "quantity": 1,
                        "subscription": "sub_1MowQVLkdIwHu7ixeRlqHVzs"
                    }
                ],
                "has_more": False,
                "url": "/v1/subscription_items?subscription=sub_1MowQVLkdIwHu7ixeRlqHVzs"
            },
            "latest_invoice": "in_1MowQVLkdIwHu7ixeRlqHVzv",
            "livemode": False,
            "metadata": {},
            "pause_collection": None,
            "pending_invoice_item_interval": None,
            "pending_setup_intent": None,
            "pending_update": None,
            "plan": {
                "id": "price_1MowQVLkdIwHu7ixeRlqHVzb",
                "object": "price",
                "active": True,
                "billing_scheme": "per_unit",
                "currency": "usd",
                "livemode": False,
                "lookup_key": None,
                "metadata": {},
                "nickname": None,
                "product": "prod_NhD8HD2bY8dP3V",
                "recurring": {
                    "aggregate_usage": None,
                    "interval": "month",
                    "interval_count": 1,
                    "usage_type": "licensed"
                },
                "tiers_mode": None,
                "transform_quantity": None,
                "type": "recurring",
                "unit_amount": 1000,
                "unit_amount_decimal": "1000"
            },
            "quantity": 1,
            "schedule": None,
            "start_date": 1643715200,
            "status": "active",
            "transfer_data": None,
            "trial_end": None,
            "trial_start": None
        }
    ]
    stripe_action.sync_batch(batch)
    ```

In this example, the `sync_batch` method is called with a list of customer data to synchronize.

### Soft Delete Subscription

The `StripeSubscriptionAction` class also provides a soft delete method, which allows you to mark a customer as deleted without actually deleting it from the local database.

**Methods:** `soft_delete(self, stripe_id: str)`

This method is used to soft delete a customer by its Stripe ID. It marks the customer as deleted in the local database.

!!! Example "Soft Delete Subscription"
    ```python
    from django_stripe.actions import StripeSubscriptionAction

    stripe_action = StripeSubscriptionAction()
    stripe_id = 'sub_1MowQVLkdIwHu7ixeRlqHVzs'
    stripe_action.soft_delete(stripe_id)
    ```

In this example, the `soft_delete` method is called with a Stripe ID to soft delete the customer.
