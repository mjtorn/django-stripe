# Actions

The `django-stripe` package provides a set of actions which are used to sync data from Stripe to the local database. Actions are designed to be used in your application code to interact with Stripe.

Actions are organized by the type of Stripe object they interact with. For example, the `StripeCustomerAction` is used to sync customer objects from Stripe to the local database.

Each action provides a set of methods which are used to perform syncing operations on the Stripe object. For example, the `StripeCustomerAction` provides methods to sync all customer objects from Stripe to the local database and to soft delete a customer object in the local database.

## Using Actions

Actions are typically used in your application code to sync data from Stripe to the local database. To use an action, you must first create an instance of the action class.

For example, to use the `StripeCustomerAction` to sync all customer objects from Stripe to the local database, you would create an instance of the action class and call the `sync_all` method:

!!! Example "Sync all customers"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    stripe_action.sync_all()
    ```
