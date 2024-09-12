Django Stripe Integrations
===========================

`django-stripe` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Management commands that help synchronize customer data, cards, subscriptions, coupons, prices, and products from Stripe.
- Built-in webhook handling for secure communication with Stripe.
- A wide range of functions for creating and managing customers, subscriptions, and other Stripe-related operations within your Django web application.

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
    "API_VERSION": "2022-11-15", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
}
```

## References
-------------

Stripe API Doc: [https://stripe.com/docs/api](https://stripe.com/docs/api)
