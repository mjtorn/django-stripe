Stripe Coupon
=====================

The `StripeCouponAction` class is a part of the Django Stripe library, which provides a set of actions for synchronizing local Stripe coupon data with the Stripe API. This class is designed to handle the complexities of retrieving and updating coupon data, making it easier to integrate Stripe with your Django application.

The `StripeCouponAction` class is defined in the `django_stripe.actions` module and has the following key characteristics:

*   **Model Class**: The `StripeCouponAction` class is associated with the `StripeCoupon` model.
*   **Stripe Object Class**: The class uses the `stripe.Coupon` object to interact with the Stripe API.
*   **Syncing Method**: The class provides a `sync_all` method to synchronize all local Stripe coupon data with the Stripe API.

Overall, the `StripeCouponAction` class provides a convenient and efficient way to manage Stripe coupon data in your Django application.

## Methods

### Sync All Coupons

**Method:** `sync_all(self)`

This method is used to synchronize all local Stripe coupons data with the Stripe API. It retrieves a batch of coupons from the Stripe API and then iterates over them, calling the `sync` method on each one.

??? example "Sync all coupons"
    ```python
    from django_stripe.actions import StripeCouponAction

    stripe_action = StripeCouponAction()
    stripe_action.sync_all()
    ```

In this example, the `sync_all` method is called to synchronize all local Stripe customer data with the Stripe API.

### Sync Coupons for given IDs

**Method:** `sync_by_ids(self, ids: list)`

This method is used to synchronize local Stripe customer data for a specific list of customer IDs. It retrieves the coupons from the Stripe API and then iterates over them, calling the `sync` method on each one.

??? example "Sync Coupons for given IDs"
    ```python
    from django_stripe.actions import StripeCouponAction

    stripe_action = StripeCouponAction()
    ids = ['jMT0WJUD', 'jMT0WJUE']
    stripe_action.sync_by_ids(ids)
    ```

In this example, the `sync_by_ids` method is called with a list of customer IDs to synchronize.

### Sync Batch of Coupons

**Methods:** `sync_batch(self, batch:list[dict])`

This method is used to synchronize a batch of local Stripe customer data. It takes a list of customer data as an argument and iterates over it, calling the `sync` method on each one.

??? example "Sync Batch of Coupons"
    ```python
    from django_stripe.actions import StripeCouponAction

    stripe_action = StripeCouponAction()
    batch = [
        {
            'id': 'jMT0WJUE',
            'object': 'coupon',
            'amount_off': 1000,
            'created': 1679431181,
            'currency': 'usd',
            'duration': 'forever',
            'duration_in_months': None,
            'livemode': False,
            'max_redemptions': None,
            'metadata': {},
            'name': None,
            'percent_off': None,
            'redeem_by': None,
            'times_redeemed': 0,
        },
        {
            'id': 'jMT0WJUD',
            'object': 'coupon',
            'amount_off': 1000,
            'created': 1679431181,
            'currency': 'usd',
            'duration': 'forever',
            'duration_in_months': None,
            'livemode': False,
            'max_redemptions': None,
            'metadata': {},
            'name': None,
            'percent_off': None,
            'redeem_by': None,
            'times_redeemed': 0,
        },
    ]
    stripe_action.sync_batch(batch)
    ```

In this example, the `sync_batch` method is called with a list of customer data to synchronize.

### Soft Delete Coupon

The `StripeCouponAction` class also provides a soft delete method, which allows you to mark a customer as deleted without actually deleting it from the local database.

**Methods:** `soft_delete(self, stripe_id: str)`

This method is used to soft delete a customer by its Stripe ID. It marks the customer as deleted in the local database.

??? example "Soft Delete Coupon"
    ```python
    from django_stripe.actions import StripeCouponAction

    stripe_action = StripeCouponAction()
    stripe_id = 'jMT0WJUD'
    stripe_action.soft_delete(stripe_id)
    ```

In this example, the `soft_delete` method is called with a Stripe ID to soft delete the customer.
