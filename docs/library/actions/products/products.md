Stripe Product
=====================

The `StripeProductAction` class is a part of the Django Stripe library, which provides a set of actions for synchronizing local Stripe product data with the Stripe API. This class is designed to handle the complexities of retrieving and updating product data, making it easier to integrate Stripe with your Django application.

The `StripeProductAction` class is defined in the `django_stripe.actions` module and has the following key characteristics:

*   **Model Class**: The `StripeProductAction` class is associated with the `StripeProduct` model.
*   **Stripe Object Class**: The class uses the `stripe.Product` object to interact with the Stripe API.
*   **Syncing Method**: The class provides a `sync_all` method to synchronize all local Stripe product data with the Stripe API.

Overall, the `StripeProductAction` class provides a convenient and efficient way to manage Stripe product data in your Django application.

## Methods

### Sync All Products

**Method:** `sync_all(self)`

This method is used to synchronize all local Stripe products data with the Stripe API. It retrieves a batch of products from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync all products"
    ```python
    from django_stripe.actions import StripeProductAction

    stripe_action = StripeProductAction()
    stripe_action.sync_all()
    ```

In this example, the `sync_all` method is called to synchronize all local Stripe customer data with the Stripe API.

### Sync Products for given IDs

**Method:** `sync_by_ids(self, ids: list)`

This method is used to synchronize local Stripe customer data for a specific list of customer IDs. It retrieves the products from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync Products for given IDs"
    ```python
    from django_stripe.actions import StripeProductAction

    stripe_action = StripeProductAction()
    ids = ['prod_123456789', 'prod_987654321']
    stripe_action.sync_by_ids(ids)
    ```

In this example, the `sync_by_ids` method is called with a list of customer IDs to synchronize.

### Sync Batch of Products

**Methods:** `sync_batch(self, batch:list[dict])`

This method is used to synchronize a batch of local Stripe customer data. It takes a list of customer data as an argument and iterates over it, calling the `sync` method on each one.

!!! Example "Sync Batch of Products"
    ```python
    from django_stripe.actions import StripeProductAction

    stripe_action = StripeProductAction()
    batch = [
        {'id': 'prod_123456789', 'name': 'Product 1', 'description': 'test product'},
        {'id': 'prod_987654321', 'name': 'Product 2', 'description': 'test product'}
    ]
    stripe_action.sync_batch(batch)
    ```

In this example, the `sync_batch` method is called with a list of customer data to synchronize.

### Soft Delete Product

The `StripeProductAction` class also provides a soft delete method, which allows you to mark a customer as deleted without actually deleting it from the local database.

**Methods:** `soft_delete(self, stripe_id: str)`

This method is used to soft delete a customer by its Stripe ID. It marks the customer as deleted in the local database.

!!! Example "Soft Delete Product"
    ```python
    from django_stripe.actions import StripeProductAction

    stripe_action = StripeProductAction()
    stripe_id = 'prod_123456789'
    stripe_action.soft_delete(stripe_id)
    ```

In this example, the `soft_delete` method is called with a Stripe ID to soft delete the customer.
