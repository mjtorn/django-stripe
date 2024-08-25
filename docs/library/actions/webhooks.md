# Webhook

With webhook actions, we can process webhook data based on its event type.

!!! Example
    ```
    from django_stripe.actions import StripeWebhook

    StripeWebhook.process_webhook(event_data)
    ```

## Process webhook

This method processes the webhook event by adding the event data to the local database. For more details, refer to the [event action](/library/actions/events/#add-event) for more details.

**Method**

```python
from django_stripe.actions import StripeWebhook

StripeWebhook.process_webhook(event_data)
```

**Returns**

`None`
