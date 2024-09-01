# Standard Library Stuff
from unittest.mock import MagicMock, patch

# Third Party Stuff
from django.test import TestCase
from django.utils import timezone

# Django Stripe Stuff
from django_stripe.actions import StripeProductAction
from django_stripe.models import StripeProduct


class StripeProductActionTestCase(TestCase):
    def setUp(self):
        self.action = StripeProductAction()

    @patch("stripe.Product.retrieve")
    def test_pre_set_defualt_syncs_product_if_not_exist(self, mock_retrieve):
        stripe_data = {"id": "prod_NWjs8kKbJWmuuc"}
        mock_product = MagicMock()
        mock_product.id = "prod_NWjs8kKbJWmuuc"
        mock_product.name = "Gold Plan"
        mock_retrieve.return_value = mock_product
        StripeProduct.objects.create(
            **{
                "stripe_id": "prod_NWjs8kKbJWmuuc",
                "active": True,
                "created": 1678833149,
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
        )

        self.action.pre_set_defualt(stripe_data)
        product = StripeProduct.objects.get(stripe_id="prod_NWjs8kKbJWmuuc")
        self.assertEqual(product.name, "Gold Plan")

    @patch("stripe.Product.retrieve")
    def test_sync_creates_or_updates_product(self, mock_retrieve):
        stripe_data = {
            "id": "prod_NWjs8kKbJWmuuc",
            "object": "product",
            "active": True,
            "created": 1678833149,
            "name": "Gold Plan",
            "description": None,
            "images": [],
            "metadata": {},
            "livemode": False,
            "updated": 1678834149,
        }
        mock_retrieve.return_value = stripe_data
        self.action.sync(stripe_data)

        product = StripeProduct.objects.get(stripe_id="prod_NWjs8kKbJWmuuc")
        self.assertEqual(product.name, "Gold Plan")
        self.assertEqual(product.livemode, False)

    @patch("stripe.Product.auto_paging_iter")
    def test_sync_all(self, mock_auto_paging_iter):
        mock_auto_paging_iter.return_value = [
            {
                "id": "prod_NWjs8kKbJWmuuc",
                "object": "product",
                "active": True,
                "created": 1678833149,
                "updated": 1678833149,
                "name": "Gold Plan",
                "description": None,
                "images": [],
                "metadata": {},
                "livemode": False,
            }
        ]
        self.action.sync_all()

        products = StripeProduct.objects.all()
        self.assertEqual(products.count(), 1)
        self.assertTrue(
            StripeProduct.objects.filter(stripe_id="prod_NWjs8kKbJWmuuc").exists()
        )

    def test_soft_delete_marks_as_deleted(self):
        product = StripeProduct.objects.create(
            **{
                "stripe_id": "prod_NWjs8kKbJWmuuc",
                "active": True,
                "created": 1678833149,
                "updated": 1678833149,
                "name": "Gold Plan",
                "description": None,
                "images": [],
                "metadata": {},
                "livemode": False,
            }
        )
        self.action.soft_delete("prod_NWjs8kKbJWmuuc")

        product.refresh_from_db()
        self.assertIsNotNone(product.date_purged)
        self.assertTrue(product.date_purged <= timezone.now())


# Include additional tests for other methods as needed.
