

StripeEventAction
================

The `StripeEventAction` class is a crucial component of the Django Stripe library, responsible for handling and processing Stripe events. This documentation provides a detailed explanation of the class, its methods, and examples of usage.

### Class Overview

The `StripeEventAction` class is defined in the `django_stripe.actions` module. It provides methods for adding and processing Stripe events, as well as linking customers to event objects.

### Methods

#### `add`

The `add` method is used to add a Stripe event to the system. It takes the following arguments:

| Argument        | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| `stripe_id`     | The ID of the Stripe event.                                                        |
| `kind`          | The type of Stripe event (e.g., `invoice.created`, `customer.updated`, etc.).     |
| `livemode`      | A boolean indicating whether the event was triggered in live mode or not.          |
| `api_version`   | The version of the Stripe API used to trigger the event.                          |
| `message`       | The data associated with the event.                                               |
| `request`       | The request object that triggered the event (optional).                           |
| `pending_webhooks` | The number of pending webhooks (optional).                                    |

!!! Example "Add Stripe event"
    ```python
    from django_stripe.actions import StripeEventAction

    stripe_id = "evt_123456789"
    kind = "invoice.created"
    livemode = True
    api_version = "2022-11-15"
    message = {"id": "in_123456789", "object": "invoice", "amount_paid": 1000}

    StripeEventAction.add(stripe_id, kind, livemode, api_version, message)
    ```

This example adds a Stripe event for an invoice creation, with the specified `stripe_id`, `kind`, `livemode`, `api_version`, and `message`.

#### `link_customer`

The `link_customer` method is used to link a customer to a Stripe event object. It takes the following argument:

| Argument        | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| `event`         | The `django_stripe.stripe.models.Event` object to link the customer to.              |

> Example:
    ```python
    from django_stripe.actions import StripeEventAction
    from django_stripe.stripe.models import Event

    event = Event.objects.get(id="evt_123456789")
    customer = Customer.objects.get(id="cu_123456789")

    StripeEventAction.link_customer(event, customer)
    ```

This example links a customer to a Stripe event object.

### Usage

The `StripeEventAction` class can be used in various scenarios, such as:

* Processing Stripe webhooks: You can use the `add` method to add Stripe events to the system when a webhook is triggered.
* Syncing Stripe data: You can use the `link_customer` method to link customers to Stripe event objects when syncing Stripe data.

### Best Practices

* Always validate the `stripe_id` and `kind` arguments before calling the `add` method.
* Use the `request` argument to pass the request object that triggered the event, if available.
* Use the `pending_webhooks` argument to pass the number of pending webhooks, if available.
* Always check the `livemode` argument to determine whether the event was triggered in live mode or not.
