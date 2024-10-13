# Standard Library Stuff
from unittest.mock import patch

# Third Party Stuff
from django.test import TestCase

# Django Stripe Stuff
from django_stripe.actions import StripeCouponAction
from django_stripe.models import StripeCoupon


class StripeCouponActionTest(TestCase):
    def setUp(self):
        self.action = StripeCouponAction()

    @patch("stripe.Coupon.retrieve")
    def test_sync(self, mock_retrieve):
        # Mocking the stripe coupon data
        stripe_data = {
            "id": "jMT0WJUD",
            "object": "coupon",
            "amount_off": None,
            "created": 1678037688,
            "currency": None,
            "duration": "repeating",
            "duration_in_months": 3,
            "livemode": False,
            "max_redemptions": None,
            "metadata": {},
            "name": None,
            "percent_off": 25.5,
            "redeem_by": None,
            "times_redeemed": 0,
            "valid": True,
        }
        mock_retrieve.return_value = stripe_data

        # Execute sync method
        self.action.sync(stripe_data)

        # Assertions
        coupon = StripeCoupon.objects.get(stripe_id="jMT0WJUD")
        self.assertEqual(coupon.amount_off, None)
        # self.assertEqual(coupon.created, convert_epoch(stripe_data["created"]))
        self.assertEqual(coupon.duration, "repeating")
        self.assertEqual(coupon.duration_in_months, 3)
        self.assertEqual(coupon.percent_off, 25.5)
        self.assertEqual(coupon.valid, True)

    @patch("stripe.Coupon.retrieve")
    def test_sync_by_ids(self, mock_retrieve):
        # Mocking the stripe coupon data
        stripe_data = {
            "id": "jMT0WJUD",
            "object": "coupon",
            "amount_off": None,
            "created": 1678037688,
            "currency": None,
            "duration": "repeating",
            "duration_in_months": 3,
            "livemode": False,
            "max_redemptions": None,
            "metadata": {},
            "name": None,
            "percent_off": 25.5,
            "redeem_by": None,
            "times_redeemed": 0,
            "valid": True,
        }
        mock_retrieve.return_value = stripe_data

        # Execute sync_by_ids method
        self.action.sync_by_ids(["jMT0WJUD"])

        # Assertions
        coupon = StripeCoupon.objects.get(stripe_id="jMT0WJUD")
        self.assertEqual(coupon.amount_off, None)
        # self.assertEqual(coupon.created, timezone.datetime.fromtimestamp(1678037688))
        self.assertEqual(coupon.duration, "repeating")
        self.assertEqual(coupon.duration_in_months, 3)
        self.assertEqual(coupon.percent_off, 25.5)
        self.assertEqual(coupon.valid, True)

    @patch("stripe.Coupon.auto_paging_iter")
    def test_sync_all(self, mock_auto_paging_iter):
        # Mocking the stripe coupons data
        stripe_coupons = [
            {
                "id": "jMT0WJUD1",
                "object": "coupon",
                "amount_off": None,
                "created": 1678037688,
                "currency": None,
                "duration": "repeating",
                "duration_in_months": 3,
                "livemode": False,
                "max_redemptions": None,
                "metadata": {},
                "name": None,
                "percent_off": 25.5,
                "redeem_by": None,
                "times_redeemed": 0,
                "valid": True,
            },
            {
                "id": "jMT0WJUD2",
                "object": "coupon",
                "amount_off": None,
                "created": 1678037690,
                "currency": None,
                "duration": "forever",
                "duration_in_months": None,
                "livemode": False,
                "max_redemptions": None,
                "metadata": {},
                "name": None,
                "percent_off": 10.0,
                "redeem_by": None,
                "times_redeemed": 1,
                "valid": True,
            },
        ]
        mock_auto_paging_iter.return_value = stripe_coupons

        # Clear existing coupons
        StripeCoupon.objects.all().delete()

        # Execute sync_all method
        self.action.sync_all()

        # Assertions
        coupons = StripeCoupon.objects.all()
        self.assertEqual(coupons.count(), 2)

        coupon1 = StripeCoupon.objects.get(stripe_id="jMT0WJUD1")
        self.assertEqual(coupon1.duration, "repeating")
        self.assertEqual(coupon1.percent_off, 25.5)

        coupon2 = StripeCoupon.objects.get(stripe_id="jMT0WJUD2")
        self.assertEqual(coupon2.duration, "forever")
        self.assertEqual(coupon2.percent_off, 10.0)

    @patch("stripe.Coupon.auto_paging_iter")
    def test_sync_all_with_deleted_objects(self, mock_auto_paging_iter):
        # Mocking the stripe coupons data
        stripe_coupons = [
            {
                "id": "jMT0WJUD1",
                "object": "coupon",
                "amount_off": None,
                "created": 1678037688,
                "currency": None,
                "duration": "repeating",
                "duration_in_months": 3,
                "livemode": False,
                "max_redemptions": None,
                "metadata": {},
                "name": None,
                "percent_off": 25.5,
                "redeem_by": None,
                "times_redeemed": 0,
                "valid": True,
            }
        ]
        mock_auto_paging_iter.return_value = stripe_coupons

        # Create a coupon that will be deleted
        StripeCoupon.objects.create(
            stripe_id="jMT0WJUD2",
            amount_off=None,
            duration="forever",
            duration_in_months=None,
            percent_off=10.0,
            valid=True,
        )

        # Execute sync_all method
        self.action.sync_all()

        # Assertions
        coupons = StripeCoupon.objects.filter(deleted_at__isnull=True)
        self.assertEqual(coupons.count(), 1)
        self.assertTrue(
            StripeCoupon.objects.filter(
                stripe_id="jMT0WJUD2", deleted_at__isnull=False
            ).exists()
        )

    @patch("stripe.Coupon.auto_paging_iter")
    def test_sync_batch(self, mock_auto_paging_iter):
        # Mocking the stripe coupons data
        stripe_coupons = [
            {
                "id": "jMT0WJUD1",
                "object": "coupon",
                "amount_off": None,
                "created": 1678037688,
                "currency": None,
                "duration": "repeating",
                "duration_in_months": 3,
                "livemode": False,
                "max_redemptions": None,
                "metadata": {},
                "name": None,
                "percent_off": 25.5,
                "redeem_by": None,
                "times_redeemed": 0,
                "valid": True,
            }
        ]
        mock_auto_paging_iter.return_value = stripe_coupons

        # Execute sync_batch method
        self.action.sync_batch(stripe_coupons)

        # Assertions
        coupon = StripeCoupon.objects.get(stripe_id="jMT0WJUD1")
        self.assertEqual(coupon.duration, "repeating")
        self.assertEqual(coupon.percent_off, 25.5)

    def test_soft_delete(self):
        # Create a coupon that will be soft-deleted
        coupon = StripeCoupon.objects.create(
            stripe_id="jMT0WJUD",
            amount_off=None,
            duration="repeating",
            duration_in_months=3,
            percent_off=25.5,
            valid=True,
        )

        # Execute soft_delete method
        self.action.soft_delete("jMT0WJUD")

        # Assertions
        coupon.refresh_from_db()
        self.assertIsNotNone(coupon.deleted_at)
