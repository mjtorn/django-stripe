# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.test import TestCase

# Django Stripe Stuff
from django_stripe.actions import StripePriceAction, StripeProductAction
from django_stripe.models import StripePrice, StripeProduct


class StripePriceActionTestCase(TestCase):
    def setUp(self):
        # Setup initial data
        self.stripe_price_data = {
            "id": "price_1MoBy5LkdIwHu7ixZhnattbh",
            "object": "price",
            "active": True,
            "billing_scheme": "per_unit",
            "created": 1679431181,
            "currency": "usd",
            "custom_unit_amount": None,
            "livemode": False,
            "lookup_key": None,
            "metadata": {},
            "nickname": None,
            "product": "prod_NWjs8kKbJWmuuc",
            "recurring": {
                "aggregate_usage": None,
                "interval": "month",
                "interval_count": 1,
                "trial_period_days": None,
                "usage_type": "licensed",
            },
            "tax_behavior": "unspecified",
            "tiers_mode": None,
            "transform_quantity": None,
            "type": "recurring",
            "unit_amount": 1000,
            "unit_amount_decimal": "1000",
        }

        # Mock product data that will be synced
        self.stripe_product_data = {
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

        # Create a corresponding product in the database
        self.product = StripeProductAction().sync(self.stripe_product_data.copy())

    @patch("stripe.Product.retrieve")
    def test_sync_creates_price(self, mock_product_retrieve):
        # Mock the Stripe API call to retrieve the product
        mock_product_retrieve.return_value = self.stripe_product_data.copy()

        # Create an instance of StripePriceAction
        action = StripePriceAction()

        # Call sync method with the price data
        action.sync(self.stripe_price_data.copy())

        # Check if the price was created in the database
        price = StripePrice.objects.get(stripe_id="price_1MoBy5LkdIwHu7ixZhnattbh")

        # Assert price fields
        self.assertEqual(price.stripe_id, self.stripe_price_data["id"])
        self.assertEqual(price.active, self.stripe_price_data["active"])
        self.assertEqual(price.billing_scheme, self.stripe_price_data["billing_scheme"])
        self.assertEqual(price.currency, self.stripe_price_data["currency"])
        self.assertEqual(price.livemode, self.stripe_price_data["livemode"])
        self.assertEqual(price.unit_amount, self.stripe_price_data["unit_amount"])
        self.assertEqual(
            int(price.unit_amount_decimal),
            int(self.stripe_price_data["unit_amount_decimal"]),
        )
        self.assertEqual(
            price.product, self.product
        )  # Ensure the product is synced correctly
        # self.assertEqual(
        #     price.recurring_interval, self.stripe_price_data["recurring"]["interval"]
        # )
        # self.assertEqual(
        #     price.recurring_interval_count,
        #     self.stripe_price_data["recurring"]["interval_count"],
        # )
        # self.assertEqual(
        #     price.recurring_usage_type,
        #     self.stripe_price_data["recurring"]["usage_type"],
        # )

    @patch("stripe.Price.retrieve")
    def test_sync_updates_existing_price(self, mock_price_retrieve):
        """Test if an existing price is updated correctly."""
        mock_price_retrieve.return_value = self.stripe_product_data.copy()

        # Create an existing price object
        existing_price = StripePrice.objects.create(
            stripe_id="price_1MoBy5LkdIwHu7ixZhnattbh",
            active=False,  # Initially set as inactive
            unit_amount=500,  # Initial unit amount
            product=self.product,
            created=1679431181,
        )

        action = StripePriceAction()
        action.sync(self.stripe_price_data.copy())

        # Assert the price was updated
        existing_price.refresh_from_db()
        self.assertEqual(existing_price.active, True)
        self.assertEqual(int(existing_price.unit_amount), 1000)

    @patch("stripe.Product.retrieve")
    def test_sync_creates_new_product_if_not_exist(self, mock_product_retrieve):
        """Test if a new product is created when it doesn't exist."""
        # Simulate the product does not exist in the database
        StripeProduct.objects.all().delete()

        mock_product_retrieve.return_value = self.stripe_product_data.copy()

        action = StripePriceAction()
        action.sync(self.stripe_price_data.copy())

        # Assert the product was created and price was associated with it
        product = StripeProduct.objects.get(stripe_id="prod_NWjs8kKbJWmuuc")
        price = StripePrice.objects.get(stripe_id="price_1MoBy5LkdIwHu7ixZhnattbh")
        self.assertEqual(price.product, product)

    @patch("stripe.Product.retrieve")
    def test_sync_batch_creates_prices(self, mock_product_retrieve):
        """Test batch synchronization of multiple prices."""
        mock_product_retrieve.return_value = self.stripe_product_data.copy()

        action = StripePriceAction()
        batch_data = [self.stripe_price_data.copy(), self.stripe_price_data.copy()]

        # Change IDs for the second price in the batch
        batch_data[1]["id"] = "price_1MoBy6LkdIwHu7ixZhnattbh"

        action.sync_batch(batch_data)

        # Assert both prices were created
        price1 = StripePrice.objects.get(stripe_id="price_1MoBy5LkdIwHu7ixZhnattbh")
        price2 = StripePrice.objects.get(stripe_id="price_1MoBy6LkdIwHu7ixZhnattbh")

        self.assertEqual(price1.currency, "usd")
        self.assertEqual(price2.currency, "usd")

    @patch("stripe.Product.retrieve")
    def test_sync_batch_updates_existing_prices(self, mock_product_retrieve):
        """Test batch synchronization updates existing prices."""
        mock_product_retrieve.return_value = self.stripe_product_data.copy()

        # Create an existing price object
        existing_price1 = StripePrice.objects.create(
            stripe_id="price_1MoBy5LkdIwHu7ixZhnattbh",
            active=False,
            currency="usd",
            unit_amount=500,
            product=self.product,
            created=1679431181,
        )

        # New price data for batch sync
        batch_data = [self.stripe_price_data.copy()]

        action = StripePriceAction()
        action.sync_batch(batch_data)

        # Assert the existing price was updated
        existing_price1.refresh_from_db()
        self.assertEqual(existing_price1.unit_amount, 1000)
        self.assertEqual(existing_price1.active, True)
