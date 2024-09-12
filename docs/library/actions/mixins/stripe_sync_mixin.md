Stripe Sync Action Mixin
======================================

`StripeSyncActionMixin` is a mixin class that provides a set of methods for synchronizing your local database via the Stripe API. It allows you to sync data from Stripe to your local database.

## Extending StripeSyncActionMixin
---------------------------------

To create your own actions, you can extend `StripeSyncActionMixin` and override the methods as needed. Here is an example:

!!! Example "Extending `StripeSyncActionMixin`"
    ```python
    from django_stripe.actions.mixins import StripeSyncActionMixin
    from django_stripe.models import StripeCustomer

    class StripeCustomerAction(StripeSyncActionMixin):
        model_class = StripeCustomer
        stripe_object_class = stripe.Customer

        def pre_set_defualt(self, stripe_data: dict):
            # Perform any necessary actions before setting default values
            print("Before setting default values")

        def set_default(self, stripe_data: dict):
            # Set default values for the local model object
            defaults = {
                "email": stripe_data["email"],
                "name": stripe_data["name"],
            }
            return defaults

        def post_set_default(self, defaults: dict):
            # Perform any necessary actions after setting default values
            print("After setting default values")
    ```

In this example, we create a `StripeCustomerAction` class that extends `StripeSyncActionMixin`. We override the `pre_set_defualt`, `set_default`, and `post_set_default` methods to perform any necessary actions.

## Using StripeSyncActionMixin
-----------------------------

To use `StripeSyncActionMixin`, you can create an instance of your action class and call the `sync` method:

!!! Example "Using methods in `StripeSyncActionMixin`"
    ```python
    from django_stripe.actions import StripeCustomerAction

    stripe_action = StripeCustomerAction()
    stripe_action.sync_all()
    ```

This will sync all the Stripe customers with the local `StripeCustomer` model.

## Methods
------------

### Sync Stripe Data

Synchronizes a local data from the Stripe API.

**Method:** `sync(self, stripe_data: dict)`

| Argument      | Description            |
| ------------- | ---------------------- |
| `stripe_data` | data from Stripe API   |

This method is the core of the mixin. It takes in Stripe data, sets default values, and then updates or creates a local model object.

### Sync data by stripe IDs

Synchronizes a local data from the Stripe API by IDs.

Method: `sync_by_ids(self, ids: list)`

| Argument | Description        |
| -------- |--------------------|
| `ids`    | list of stripe IDs |

This method is similar to `sync`, but it takes in a list of IDs instead of Stripe data.

### Set default values

**Method:** `set_default(self, stripe_data: dict)`

Sets default values for the local model object.

| Argument      | Description            |
| ------------- | ---------------------- |
| `stripe_data` | data from Stripe API   |

This method is called by `sync` and allows you to set default values for the local model object.

### Pre-processing setting default values

**Method:** `pre_set_defualt(self, stripe_data: dict)`

Called before setting default values.

| Argument      | Description            |
| ------------- | ---------------------- |
| `stripe_data` | data from Stripe API   |

This method is called by `sync` and allows you to perform any necessary actions before setting default values.

### Post-processing setting default values

**Method:** `post_set_default(self, defaults: dict)`

Called after setting default values.

| Argument | Description                                          |
| -------- |------------------------------------------------------|
| `defaults` | default values that we got from `set_default` method |

This method is called by `sync` and allows you to perform any necessary actions after setting default values.

## Customizing the Mixin
-------------------------

You can customize the mixin by overriding the `sync` method or adding new methods to the class. For example, you can add a new method to handle the syncing of related objects.

!!! Example
    ```python
    import stripe
    from django_stripe.actions.mixins import StripeSyncActionMixin
    from django_stripe.models import MyStripeModel

    class MyStripeAction(StripeSyncActionMixin):
        model_class = MyStripeModel # Your model class
        stripe_object_class = stripe.Customer # Your Stripe object class

        def sync(self, stripe_data: dict):
            # Call the parent method to sync the data
            super().sync(stripe_data)

            # Sync related objects
            related_objects = self.model_class.related_objects.filter(stripe_id=stripe_data["id"])
            related_objects.sync(stripe_data)
    ```

## Best Practices
-----------------

* Use `sync` method to sync data
* Use `set_default` method to set default values
* Use `pre_set_defualt` method to perform any necessary actions before setting default values
* Use `post_set_default` method to perform any necessary actions after setting default values
* Use `sync_by_ids` method to sync data by IDs
* Use `sync_all` method to sync all data from Stripe
