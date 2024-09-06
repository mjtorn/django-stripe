# Django Stripe

`django-stripe` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Management commands that help synchronize customer data, cards, subscriptions, coupons, prices, and products from Stripe.
- Built-in webhook handling for secure communication with Stripe.
- A wide range of functions for creating and managing customers, subscriptions, and other Stripe-related operations within your Django web application.

## Table of Contents

- [💾 Installation](#-installation)
- [🚀 Quickstart](#-quickstart)
- [📜 Code of Conduct](#code-of-conduct)

## 💾 Installation

You can easily install or upgrade to the latest version of the package using pip:

```
pip install django-stripe
```

## 🚀 Quickstart

To get started quickly, follow these steps:

1. Install the package using pip:

```commandline
pip install django-stripe
```

2. Add `django_stripe` to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...,
    'django_stripe',
]
```

3. Database migration

After implementing the models, create a migration file using the following command:

```
python manage.py makemigrations
```

Once the migration file has been created, apply the migrations to the database using the following command:

```
python manage.py migrate
```

4. In your settings, update the model paths in `STRIPE_CONFIG`:

```python
STRIPE_CONFIG = {
    "API_VERSION": "2022-11-15", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
}
```

5. Implement APIs

You can use the appropriate actions to build payment APIs. Here are some examples:

- Creating a customer

```python
from django_stripe.actions.core import StripeCustomerAction

# Pass user model instance and email as argument
customer = StripeCustomerAction(user).create(billing_email)
```

- Creating a subscription

```python
from django_stripe.actions.billings import StripeSubscriptionAction

# Pass customer model instance and prices(List of stripe price ids) to subscribe as argument
subscription = StripeSubscriptionAction.create(customer, prices)
```

## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, we have a code of conduct, which can be found [here](CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python and `django-stripe` with you.
