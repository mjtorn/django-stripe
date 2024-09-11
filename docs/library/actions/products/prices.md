Stripe Price
=====================

The `StripePriceAction` class is a part of the Django Stripe library, which provides a set of actions for synchronizing local Stripe price data with the Stripe API. This class is designed to handle the complexities of retrieving and updating price data, making it easier to integrate Stripe with your Django application.

The `StripePriceAction` class is defined in the `django_stripe.actions` module and has the following key characteristics:

*   **Model Class**: The `StripePriceAction` class is associated with the `StripePrice` model.
*   **Stripe Object Class**: The class uses the `stripe.Price` object to interact with the Stripe API.
*   **Syncing Method**: The class provides a `sync_all` method to synchronize all local Stripe price data with the Stripe API.

Overall, the `StripePriceAction` class provides a convenient and efficient way to manage Stripe price data in your Django application.

## Methods

### Sync All Prices

**Method:** `sync_all(self)`

This method is used to synchronize all local Stripe prices data with the Stripe API. It retrieves a batch of prices from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync all prices"
    ```python
    from django_stripe.actions import StripePriceAction

    stripe_action = StripePriceAction()
    stripe_action.sync_all()
    ```

In this example, the `sync_all` method is called to synchronize all local Stripe customer data with the Stripe API.

### Sync Prices for given IDs

**Method:** `sync_by_ids(self, ids: list)`

This method is used to synchronize local Stripe customer data for a specific list of customer IDs. It retrieves the prices from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync Prices for given IDs"
    ```python
    from django_stripe.actions import StripePriceAction

    stripe_action = StripePriceAction()
    ids = ['price_1MoBy6LkdIwHu7ixZhnattbe', 'price_1MoBy6LkdIwHu7ixZhnattbh']
    stripe_action.sync_by_ids(ids)
    ```

In this example, the `sync_by_ids` method is called with a list of customer IDs to synchronize.

### Sync Batch of Prices

**Methods:** `sync_batch(self, batch:list[dict])`

This method is used to synchronize a batch of local Stripe customer data. It takes a list of customer data as an argument and iterates over it, calling the `sync` method on each one.

!!! Example "Sync Batch of Prices"
    ```python
    from django_stripe.actions import StripePriceAction

    stripe_action = StripePriceAction()
    batch = [
        {
            'id': 'price_1MoBy5LkdIwHu7ixZhnattbh',
            'object': 'price',
            'active': True,
            'billing_scheme': 'per_unit',
            'created': 1679431181,
            'currency': 'usd',
            'custom_unit_amount': None,
            'livemode': False,
            'lookup_key': None,
            'metadata': {},
            'nickname': None,
            'product': 'prod_NWjs8kKbJWmuuc',
            'recurring': {
                'aggregate_usage': None,
                'interval': 'month',
                'interval_count': 1,
                'trial_period_days': None,
                'usage_type': 'licensed',
            },
            'tax_behavior': 'unspecified',
            'tiers_mode': None,
            'transform_quantity': None,
            'type': 'recurring',
            'unit_amount': 1000,
            'unit_amount_decimal': '1000',
        },
        {
            'id': 'price_1MoBy6LkdIwHu7ixZhnattbh',
            'object': 'price',
            'active': True,
            'billing_scheme': 'per_unit',
            'created': 1679431181,
            'currency': 'usd',
            'custom_unit_amount': None,
            'livemode': False,
            'lookup_key': None,
            'metadata': {},
            'nickname': None,
            'product': 'prod_NWjs8kKbJWmuuc',
            'recurring': {
                'aggregate_usage': None,
                'interval': 'month',
                'interval_count': 1,
                'trial_period_days': None,
                'usage_type': 'licensed',
            },
            'tax_behavior': 'unspecified',
            'tiers_mode': None,
            'transform_quantity': None,
            'type': 'recurring',
            'unit_amount': 1000,
            'unit_amount_decimal': '1000',
        },
    ]
    stripe_action.sync_batch(batch)
    ```

In this example, the `sync_batch` method is called with a list of customer data to synchronize.

### Soft Delete Price

The `StripePriceAction` class also provides a soft delete method, which allows you to mark a customer as deleted without actually deleting it from the local database.

**Methods:** `soft_delete(self, stripe_id: str)`

This method is used to soft delete a customer by its Stripe ID. It marks the customer as deleted in the local database.

!!! Example "Soft Delete Price"
    ```python
    from django_stripe.actions import StripePriceAction

    stripe_action = StripePriceAction()
    stripe_id = 'price_1MoBy6LkdIwHu7ixZhnattbh'
    stripe_action.soft_delete(stripe_id)
    ```

In this example, the `soft_delete` method is called with a Stripe ID to soft delete the customer.
