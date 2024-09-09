# Third Party Stuff
from unittest.mock import patch

from django.test import TestCase

# Django Stripe Stuff
from django_stripe.actions import StripeProductAction
from django_stripe.models import StripeProduct


class StripeProductActionTestCase(TestCase):
    def setUp(self):
        # Initialize StripeProductAction
        self.action = StripeProductAction()

    @patch("django_stripe.actions.StripeProductAction.stripe_object_class")
    def test_sync(self, mock_stripe_object_class):
        # Mock Stripe API response for a product
        stripe_product_data = {
            "id": "prod_NWjs8kKbJWmuuc",
            "object": "product",
            "active": True,
            "created": 1678833149,
            "default_price": None,
            "description": None,
            "images": [],
            "livemode": False,
            "metadata": {},
            "name": "Gold Plan",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "unit_label": None,
            "updated": 1678833149,
            "url": None,
        }

        # Mock the retrieve method of the stripe_object_class
        mock_stripe_object_class.retrieve.return_value = stripe_product_data

        # Sync the product data
        product = self.action.sync(stripe_product_data.copy())

        # Assert the product is created and synced in the database
        self.assertEqual(product.stripe_id, stripe_product_data["id"])
        self.assertEqual(product.name, stripe_product_data["name"])
        self.assertEqual(product.active, stripe_product_data["active"])
        # self.assertIsNone(product.default_price)
        self.assertEqual(product.description, "")

    @patch("django_stripe.actions.StripeProductAction.stripe_object_class")
    def test_sync_updates_existing_product(self, mock_stripe_object_class):
        # Create an existing product in the database
        existing_product = StripeProduct.objects.create(
            stripe_id="prod_NWjs8kKbJWmuuc",
            name="Old Plan",
            active=False,
            created=1678833149,
            updated=1678833149,
        )

        # Mock Stripe API response with updated data
        updated_stripe_product_data = {
            "id": "prod_NWjs8kKbJWmuuc",
            "object": "product",
            "active": True,
            "created": 1678833149,
            "default_price": None,
            "description": "Updated description",
            "images": [],
            "livemode": False,
            "metadata": {},
            "name": "Gold Plan",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "unit_label": None,
            "updated": 1678834149,
            "url": None,
        }

        # Mock the retrieve method of the stripe_object_class
        mock_stripe_object_class.retrieve.return_value = updated_stripe_product_data

        # Sync the updated product data
        self.action.sync(updated_stripe_product_data.copy())
        existing_product.refresh_from_db()

        # Assert the product is updated in the database
        self.assertEqual(existing_product.stripe_id, updated_stripe_product_data["id"])
        self.assertEqual(existing_product.name, updated_stripe_product_data["name"])
        self.assertEqual(existing_product.active, updated_stripe_product_data["active"])
        self.assertEqual(
            existing_product.description, updated_stripe_product_data["description"]
        )

    @patch("django_stripe.actions.StripeProductAction.stripe_object_class")
    def test_sync_creates_new_product(self, mock_stripe_object_class):
        # Mock a new Stripe product API response
        new_stripe_product_data = {
            "id": "prod_NEW8kKbJWmuuc",
            "object": "product",
            "active": True,
            "created": 1680000000,
            "default_price": None,
            "description": "New product description",
            "images": [],
            "livemode": False,
            "metadata": {},
            "name": "Silver Plan",
            "package_dimensions": None,
            "shippable": None,
            "statement_descriptor": None,
            "tax_code": None,
            "unit_label": None,
            "updated": 1680000000,
            "url": None,
        }

        # Mock the retrieve method of the stripe_object_class
        mock_stripe_object_class.retrieve.return_value = new_stripe_product_data

        # Sync the new product data
        new_product = self.action.sync(new_stripe_product_data.copy())

        # Assert the new product is created in the database
        self.assertEqual(new_product.stripe_id, new_stripe_product_data["id"])
        self.assertEqual(new_product.name, new_stripe_product_data["name"])
        self.assertEqual(new_product.active, new_stripe_product_data["active"])
        self.assertEqual(
            new_product.description, new_stripe_product_data["description"]
        )
