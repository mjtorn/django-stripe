Django Stripe
===========================

__Version:__ 0.1.2

`django-stripe` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Actions that help synchronize customers, subscriptions, coupons, prices, and products data from Stripe.
- Built-in webhook handling for secure communication with Stripe.

## Installation
---------------

You can easily install or upgrade to the latest version of the package using pip:

```
pip install django-stripe
```

## Configuration
----------------

In your settings, update `STRIPE_CONFIG`:

```python
STRIPE_CONFIG = {
    "API_VERSION": "2024-06-20", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
}
```

## References
-------------

**Stripe API Doc:** [https://stripe.com/docs/api](https://stripe.com/docs/api)
