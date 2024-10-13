# # Standard Library
# from unittest import mock
#
# # Third Party Stuff
# from django.test import TestCase
# from django.utils import timezone
#
# # Django Stripe Stuff
# from django_stripe.models import StripeCard, StripeCustomer
# from django_stripe.actions import StripeCardAction
#
#
# class StripeCardActionTestCase(TestCase):
#     def setUp(self):
#         self.customer = StripeCustomer.objects.create(stripe_id="cus_NhD8HD2bY8dP3V")
#         self.stripe_card_data = {
#             "id": "card_1MvoiELkdIwHu7ixOeFGbN9D",
#             "object": "card",
#             "brand": "Visa",
#             "country": "US",
#             "customer": self.customer.stripe_id,
#             "exp_month": 4,
#             "exp_year": 2024,
#             "fingerprint": "mToisGZ01V71BCos",
#             "funding": "credit",
#             "last4": "4242",
#             "metadata": {},
#         }
#         self.action = StripeCardAction(customer=self.customer)
#
#     @mock.patch("stripe.Customer.delete_source")
#     def test_delete_card(self, mock_delete_source):
#         # Setup the StripeCard in the local database
#         stripe_card = StripeCard.objects.create(
#             stripe_id=self.stripe_card_data["id"], customer=self.customer
#         )
#
#         # Delete the card using the action
#         self.action.delete(stripe_card.stripe_id)
#
#         # Assertions
#         mock_delete_source.assert_called_once_with(
#             self.customer.stripe_id, stripe_card.stripe_id
#         )
#         self.assertFalse(
#             StripeCard.objects.filter(stripe_id=stripe_card.stripe_id).exists()
#         )
#
#     @mock.patch("stripe.Customer.delete_source")
#     def test_delete_card_non_existent(self, mock_delete_source):
#         # Attempt to delete a non-existent card
#         self.action.delete("non_existent_card_id")
#
#         # Assertions
#         mock_delete_source.assert_called_once_with(
#             self.customer.stripe_id, "non_existent_card_id"
#         )
#         self.assertFalse(
#             StripeCard.objects.filter(stripe_id="non_existent_card_id").exists()
#         )
#
#     @mock.patch("stripe.Customer.delete_source")
#     def test_delete_card_api_error(self, mock_delete_source):
#         # Setup a scenario where the Stripe API throws an error
#         mock_delete_source.side_effect = stripe.error.StripeError("API error")
#
#         # Attempt to delete the card and handle the error
#         with self.assertRaises(stripe.error.StripeError):
#             self.action.delete(self.stripe_card_data["id"])
#
#         # Assertions
#         mock_delete_source.assert_called_once_with(
#             self.customer.stripe_id, self.stripe_card_data["id"]
#         )
#
#     @mock.patch("stripe.Customer.retrieve")
#     def test_sync_card(self, mock_retrieve):
#         # Mock the Stripe API response
#         mock_retrieve.return_value = self.stripe_card_data
#
#         # Sync the card data
#         stripe_card = self.action.sync(self.stripe_card_data)
#
#         # Assertions
#         self.assertEqual(stripe_card.stripe_id, self.stripe_card_data["id"])
#         self.assertEqual(stripe_card.brand, self.stripe_card_data["brand"])
#         self.assertEqual(stripe_card.exp_year, self.stripe_card_data["exp_year"])
#
#     @mock.patch("stripe.Customer.retrieve")
#     def test_sync_card_updates_existing(self, mock_retrieve):
#         # Setup an existing card in the database
#         existing_card = StripeCard.objects.create(
#             stripe_id=self.stripe_card_data["id"],
#             customer=self.customer,
#             brand="Mastercard",
#         )
#
#         # Mock the Stripe API response
#         mock_retrieve.return_value = self.stripe_card_data
#
#         # Sync the card data, which should update the existing card
#         stripe_card = self.action.sync(self.stripe_card_data)
#
#         # Assertions
#         self.assertEqual(
#             stripe_card.id, existing_card.id
#         )  # Ensure the same object is updated
#         self.assertEqual(
#             stripe_card.brand, self.stripe_card_data["brand"]
#         )  # Brand should be updated to "Visa"
#
#     @mock.patch("stripe.Customer.retrieve")
#     def test_sync_batch(self, mock_retrieve):
#         # Setup a batch of cards
#         card_1 = self.stripe_card_data
#         card_2 = card_1.copy()
#         card_2["id"] = "card_2"
#         mock_retrieve.return_value = [card_1, card_2]
#
#         # Sync the batch of cards
#         self.action.sync_batch([card_1, card_2])
#
#         # Assertions
#         self.assertTrue(StripeCard.objects.filter(stripe_id=card_1["id"]).exists())
#         self.assertTrue(StripeCard.objects.filter(stripe_id=card_2["id"]).exists())
#
#     @mock.patch("stripe.Customer.retrieve")
#     def test_sync_all(self, mock_retrieve):
#         # Mock a paginated iterator from the Stripe API
#         mock_retrieve.return_value.auto_paging_iter.return_value = [
#             self.stripe_card_data
#         ]
#
#         # Sync all cards
#         self.action.sync_all()
#
#         # Assertions
#         self.assertTrue(
#             StripeCard.objects.filter(stripe_id=self.stripe_card_data["id"]).exists()
#         )
#         self.assertEqual(StripeCard.objects.count(), 1)
#
#     def test_sync_deleted_cards(self):
#         # Setup a card in the local database that should be deleted
#         stripe_card = StripeCard.objects.create(
#             stripe_id="card_to_delete", customer=self.customer
#         )
#
#         # Sync with no matching card in Stripe, simulating a deletion
#         self.action.sync_all()
#
#         # Assertions
#         stripe_card.refresh_from_db()
#         self.assertIsNotNone(stripe_card.deleted_at)
#         self.assertTrue(stripe_card.deleted_at <= timezone.now())
