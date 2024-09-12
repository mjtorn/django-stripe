Quickstart
==========

## Installation
---------------

Install the package using pip:

```commandline
pip install django-stripe
```

## Update Installed Apps

Add `django_stripe` to your `INSTALLED_APPS` setting in your Django project's settings file:

```python
INSTALLED_APPS = [
    ...,
    'django_stripe',
]
```

## Database migration

After implementing the models, create a migration file using the following command:

```
python manage.py makemigrations
```

Once the migration file has been created, apply the migrations to the database using the following command:

```
python manage.py migrate
```

## Update Settings

In your Django project's settings file, update the model paths in `STRIPE_CONFIG`:

```python
STRIPE_CONFIG = {
    "API_VERSION": "2022-11-15", # Stripe API Version
    "API_KEY": "api_key", # Stripe Secret Key
}
```

## Implement APIs

You can use the appropriate actions to build payment APIs. Here are some examples:

### Syncing a customer

```python
from django.contrib.auth.models import  User
from django_stripe.actions import StripeCustomerAction
from django_stripe.models import StripeCustomer
import stripe

user = User.objects.get(email="test@example.com")
action = StripeCustomerAction()
stripe_customer = StripeCustomer.objects.get(user=user)

stripe_customer_data = stripe.Customer.retrieve(stripe_customer.stripe_id)

# Pass user model instance and email as argument
customer = StripeCustomerAction().sync(stripe_data=stripe_customer_data)
```
