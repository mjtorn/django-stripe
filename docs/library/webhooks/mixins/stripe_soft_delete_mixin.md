StripeSoftDeleteMixin Documentation
======================================

The `StripeSoftDeleteMixin` is a mixin class that provides a soft delete method for Stripe objects. This mixin is designed to be used with Django models and allows developers to mark Stripe objects as deleted without actually deleting them from the local database.

## Extending the Mixin
----------------------

To extend the `StripeSoftDeleteMixin` and build your own action, you need to create a new class that inherits from the mixin and defines the `model_class` attribute. The `model_class` attribute should be set to the Django model that you want to use with the mixin.

!!! Example
    ```python
    from django_stripe.actions import StripeSoftDeleteActionMixin
    from django_stripe.models import MyStripeModel

    class MyStripeAction(StripeSoftDeleteActionMixin):
        model_class = MyStripeModel

    my_action = MyStripeAction()
    stripe_id = 'cus_123456789'
    my_action.soft_delete(stripe_id)
    ```

## Methods
------------

### Soft Delete Stripe Object

This method is used to soft delete a Stripe object by its Stripe ID. It marks the object as deleted in the local database by setting the `date_purged` field to the current timestamp.

**Method:** `soft_delete(self, stripe_id: str)`

| Argument    | Description |
|-------------| --- |
| `stripe_id` | The Stripe ID of the object to be deleted. |

!!! Example
    ```python
    from django_stripe.actions.mixins import StripeSoftDeleteActionMixin

    class MyStripeAction(StripeSoftDeleteActionMixin):
        model_class = MyStripeModel

    my_action = MyStripeAction()
    stripe_id = 'cus_123456789'
    my_action.soft_delete(stripe_id)
    ```

## Customizing the Mixin
-------------------------

You can customize the mixin by overriding the `soft_delete` method or adding new methods to the class. For example, you can add a new method to handle the deletion of related objects.

**Example**
```python
from django_stripe.actions.mixins import StripeSoftDeleteActionMixin
from django_stripe.models import MyStripeModel

class MyStripeAction(StripeSoftDeleteActionMixin):
    model_class = MyStripeModel

    def soft_delete(self, stripe_id: str):
        # Call the parent method to mark the object as deleted
        super().soft_delete(stripe_id)

        # Delete related objects
        related_objects = self.model_class.related_objects.filter(stripe_id=stripe_id)
        related_objects.delete()

my_action = MyStripeAction()
stripe_id = 'cus_123456789'
my_action.soft_delete(stripe_id)
```

## Best Practices
------------------

* Always use the `soft_delete` method to mark objects as deleted, rather than deleting them directly.
* Use the `model_class` attribute to specify the Django model that you want to use with the mixin.
* Override the `soft_delete` method or add new methods to the class to customize the mixin.
* Use the `super()` function to call the parent method when overriding the `soft_delete` method.
