# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel


class AbstractStripeCard(AbstractStripeModel):
    """
    We can store multiple cards on a customer in order to charge the customer later.
    We can also store multiple debit cards
    on a recipient in order to transfer to those cards later.
    Stripe documentation: https://stripe.com/docs/api/cards
    """

    name = models.TextField(null=True, blank=True)
    address_line_1 = models.TextField(null=True, blank=True)
    address_line_1_check = models.CharField(null=True, blank=True, max_length=64)
    address_line_2 = models.TextField(null=True, blank=True)
    address_city = models.TextField(null=True, blank=True)
    address_state = models.TextField(null=True, blank=True)
    address_country = models.TextField(null=True, blank=True)
    address_zip = models.TextField(null=True, blank=True)
    address_zip_check = models.CharField(null=True, blank=True, max_length=64)
    brand = models.TextField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=2)
    cvc_check = models.CharField(max_length=32, blank=True, null=True)
    dynamic_last4 = models.CharField(max_length=4, blank=True, null=True)
    tokenization_method = models.CharField(max_length=32, blank=True, null=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(max_length=15, blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    fingerprint = models.TextField(blank=True, null=True)

    def __repr__(self):
        return "Card(pk={!r}, customer={!r})".format(
            self.pk,
            getattr(self, "customer", None),
        )

    class Meta:
        abstract = True
