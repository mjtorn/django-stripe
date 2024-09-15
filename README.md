# Django Stripe

[![Build Status](https://github.com/purnendukar/django-stripe/actions/workflows/django-package.yml/badge.svg)](https://github.com/purnendukar/django-stripe/actions/workflows/django-package.yml)
[![codecov](https://codecov.io/github/purnendukar/django-stripe/graph/badge.svg?token=DCKZTJ86YG)](https://codecov.io/github/purnendukar/django-stripe)

`django-stripe` is an open source Python package that simplifies the integration of Stripe payments into your Django web application. Its key features include:

- Full support for Stripe's B2C Subscription.
- Built-in webhook handling for secure communication with Stripe.
- A wide range of functions for creating and managing customers, subscriptions, and other Stripe-related operations within your Django web application.

## Table of Contents

- [💾 Installation](#-installation)
- [🚀 Quickstart](#-quickstart)
- [📜 Code of Conduct](#code-of-conduct)

## 💾 Installation

You can easily install or upgrade to the latest version of the package using pip:

```
pip install django-stripe-plus
```

## 🚀 Quickstart

To get started quickly, follow these steps:

1. Install the package using pip:

```commandline
pip install django-stripe-plus
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
    "API_VERSION": "2024-06-20", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
}
```

5. Implement APIs

You can use the appropriate actions to build payment APIs. Here are some examples:
You can use the appropriate actions to build payment APIs. Here are some examples:

- Syncing a customer

```python
from django.contrib.auth.models import  User
from django_stripe.actions import StripeCustomerAction
from django_stripe.models import StripeCustomer
import stripe

user = User.objects.get(email="test@example.com")
action = StripeCustomerAction()
stripe_customer = StripeCustomer.objects.get(user=user)

stripe_customer_data = stripe.Customer.retrieve(stripe_customer.stripe_id)

customer = StripeCustomerAction().sync(stripe_data=stripe_customer_data)
```

## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, we have a code of conduct, which can be found [here](CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python and `django-stripe` with you.
