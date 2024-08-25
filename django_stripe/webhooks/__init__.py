# Standard Library
import importlib

importlib.import_module("django_stripe.webhooks.products")
importlib.import_module("django_stripe.webhooks.customers")
importlib.import_module("django_stripe.webhooks.subscriptions")
importlib.import_module("django_stripe.webhooks.prices")
importlib.import_module("django_stripe.webhooks.sources")
importlib.import_module("django_stripe.webhooks.coupons")
