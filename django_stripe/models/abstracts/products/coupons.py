# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel
from django_stripe.utils import CURRENCY_SYMBOLS, Currency


class AbstractStripeCoupon(AbstractStripeModel):
    """
    A coupon contains information about a percent-off or
    amount-off discount we might want to apply to a customer.

    Coupons may be applied to invoices or orders.
    Coupons do not work with conventional one-off charges.

    Stripe documentation: https://stripe.com/docs/api/coupons
    """

    ONCE = "once"
    REPEATING = "repeating"
    FOREVER = "forever"

    STRIPE_COUPON_DURATION_TYPES = (
        (ONCE, "Once"),
        (REPEATING, "Repeating"),
        (FOREVER, "Forever"),
    )

    name = models.CharField(
        max_length=64,
        blank=True,
        help_text=(
            "Name of the coupon displayed to customers "
            "on for instance invoices or receipts"
        ),
    )
    applies_to = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Contains information about what product this coupon applies to. "
            "This field is not included by default. "
            "To include it in the response, expand the applies_to field"
        ),
    )
    amount_off = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=True,
        blank=True,
        help_text=(
            "Amount (in the currency specified) "
            "that will be taken off the subtotal "
            "of any invoices for this customer"
        ),
    )
    currency = models.CharField(
        choices=Currency.choices,
        default=Currency.USD.value,
        max_length=3,
        help_text=(
            "If amount_off has been set, the three-letter ISO code "
            "for the currency of the amount to take off"
        ),
    )
    duration = models.CharField(
        choices=STRIPE_COUPON_DURATION_TYPES,
        max_length=16,
        default="once",
        help_text=(
            "One of forever, once, and repeating. "
            "Describes how long a customer who applies this coupon "
            "will get the discount"
        ),
    )
    duration_in_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "Required only if duration is repeating, "
            "in which case it must be a positive integer that "
            "specifies the number of months the discount will be in effect"
        ),
    )
    max_redemptions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="A positive integer specifying the number of times the coupon can "
        "be redeemed before it’s no longer valid",
    )
    percent_off = models.FloatField(
        null=True,
        blank=True,
        help_text="Percent that will be taken off the subtotal of any invoices "
        "for this customer for the duration of the coupon",
    )
    redeem_by = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date after which the coupon can no longer be redeemed",
    )
    times_redeemed = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of times this coupon has been applied to a customer",
    )

    valid = models.BooleanField(default=False)

    def __str__(self):
        if self.amount_off is None:
            description = "{}% off".format(
                self.percent_off,
            )
        else:
            description = "{}{}".format(
                CURRENCY_SYMBOLS.get(self.currency, ""), self.amount_off
            )

        return "Coupon for {}, {}".format(description, self.duration)

    class Meta:
        abstract = True
