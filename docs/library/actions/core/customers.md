Stripe Customer Action
========================

The `StripeCustomerAction` class is a part of the Django Stripe library, which provides a set of actions for synchronizing local Stripe customer data with the Stripe API. This class is designed to handle the complexities of retrieving and updating customer data, making it easier to integrate Stripe with your Django application.

The `StripeCustomerAction` class is defined in the `django_stripe.actions` module and has the following key characteristics:

*   **Model Class**: The `StripeCustomerAction` class is associated with the `StripeCustomer` model.
*   **Stripe Object Class**: The class uses the `stripe.Customer` object to interact with the Stripe API.
*   **Syncing Method**: The class provides a `sync_all` method to synchronize all local Stripe customer data with the Stripe API.

Overall, the `StripeCustomerAction` class provides a convenient and efficient way to manage Stripe customer data in your Django application.

## Methods

### Sync All Customers

**Method:** `sync_all(self)`

This method is used to synchronize all local Stripe customer data with the Stripe API. It retrieves a batch of customers from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync all customers"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    stripe_action.sync_all()
    ```

In this example, the `sync_all` method is called to synchronize all local Stripe customer data with the Stripe API.

### Sync Customers for given IDs

**Method:** `sync_by_ids(self, ids: list)`

This method is used to synchronize local Stripe customer data for a specific list of customer IDs. It retrieves the customers from the Stripe API and then iterates over them, calling the `sync` method on each one.

!!! Example "Sync Customers for given IDs"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    ids = ['cus_123456789', 'cus_987654321']
    stripe_action.sync_by_ids(ids)
    ```

In this example, the `sync_by_ids` method is called with a list of customer IDs to synchronize.

### Sync Batch of Customers

**Methods:** `sync_batch(self, batch:list[dict])`

This method is used to synchronize a batch of local Stripe customer data. It takes a list of customer data as an argument and iterates over it, calling the `sync` method on each one.

!!! Example "Sync Batch of Customers"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    batch = [
        {'id': 'cus_123456789', 'name': 'John Doe', 'email': 'john.doe@example.com'},
        {'id': 'cus_987654321', 'name': 'Jane Doe', 'email': 'jane.doe@example.com'}
    ]
    stripe_action.sync_batch(batch)
    ```

In this example, the `sync_batch` method is called with a list of customer data to synchronize.

### Soft Delete Customer

The `StripeCustomerAction` class also provides a soft delete method, which allows you to mark a customer as deleted without actually deleting it from the local database.

**Methods:** `soft_delete(self, stripe_id: str)`

This method is used to soft delete a customer by its Stripe ID. It marks the customer as deleted in the local database.

!!! Example "Soft Delete Customer"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    stripe_id = 'cus_123456789'
    stripe_action.soft_delete(stripe_id)
    ```

In this example, the `soft_delete` method is called with a Stripe ID to soft delete the customer.
