# Third Party Stuff
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Django Stripe Stuff
from django_stripe.models.base.mixins import StripeBaseModel
from django_stripe.utils import CURRENCY_SYMBOLS

USD = "usd"
CURRENCY_CHOICES = ((USD, "USD"),)
DEFAULT_CURRENCY = USD


class StripeBaseProduct(StripeBaseModel):
    """
    Products describe the specific goods or services you offer to your customers.
    For example, you might offer a Standard and
    Premium version of your goods or service;
    each version would be a separate Product.
    They can be used in conjunction with Prices
    to configure pricing in Payment Links, Checkout, and Subscriptions.
    Stripe documentation: https://stripe.com/docs/api/products
    """

    active = models.BooleanField(
        help_text=("Whether the product is currently available for purchase."),
    )
    description = models.TextField(
        null=True,
        help_text=(
            "The product’s description, meant to be displayable to the customer. "
            "Use this field to optionally store a long form explanation "
            "of the product being sold for your own rendering purposes."
        ),
    )
    name = models.CharField(
        max_length=255,
        help_text=(
            "The product’s name, meant to be displayable to the customer. "
            "Whenever this product is sold via a subscription, "
            "name will show up on associated invoice line item descriptions."
        ),
    )

    statement_descriptor = models.TextField(
        null=True,
        help_text=(
            "Extra information about a product which will appear "
            "on your customer’s credit card statement."
            "In the case that multiple products are billed at once, "
            "the first statement descriptor will be used."
        ),
    )
    tax_code = models.CharField(max_length=255, null=True, help_text="A tax code ID.")
    unit_label = models.CharField(
        max_length=255,
        null=True,
        help_text=(
            "A label that represents units of this product in Stripe"
            " and on customers’ receipts and invoices."
            "When set, this will be included in associated "
            "invoice line item descriptions."
        ),
    )
    images = ArrayField(
        models.CharField(max_length=255),
        size=8,
        default=list,
        help_text=(
            "A list of up to 8 URLs of images for this product, "
            "meant to be displayable to the customer."
        ),
    )
    shippable = models.BooleanField(
        null=True, help_text="Whether this product is shipped (i.e., physical goods)."
    )
    package_dimensions = models.JSONField(
        null=True,
        help_text="The dimensions of this product for shipping purposes.",
    )
    url = models.URLField(
        max_length=500,
        null=True,
        help_text="A URL of a publicly-accessible webpage for this product.",
    )
    created = models.BigIntegerField(
        help_text=(
            "Time at which the object was created. "
            "Measured in seconds since the Unix epoch"
        )
    )
    updated = models.BigIntegerField(
        help_text=(
            "Time at which the object was last updated. "
            "Measured in seconds since the Unix epoch"
        )
    )

    class Meta:
        abstract = True


class StripeBasePrice(StripeBaseModel):
    """
    Prices define the unit cost, currency, and (optional) billing cycle for both
    recurring and one-time purchases of products. Products help you track inventory
    or provisioning, and prices help you track payment terms. Different physical
    goods or levels of service should be represented by products, and pricing options
    should be represented by prices. This approach lets you change prices without
    having to change your provisioning scheme.

    For example,
    you might have a single "gold" product that has
    prices for $10/month, $100/year, and €9 once.
    Stripe documentation: https://stripe.com/docs/api/prices
    """

    ONE_TIME = "one_time"
    RECURRING = "recurring"

    PRICE_TYPES = [
        (ONE_TIME, "One Time"),
        (RECURRING, "Recurring"),
    ]

    TAX_INCLUSIVE = "inclusive"
    TAX_EXCLUSIVE = "exclusive"
    TAX_UNSPECIFIED = "unspecified"

    TAX_BEHAVIOR_TYPES = [
        (TAX_INCLUSIVE, "TAX Inclusive"),
        (TAX_EXCLUSIVE, "TAX Exclusive"),
        (TAX_INCLUSIVE, "TAX Unspecified"),
    ]

    PER_UNIT = "per_unit"
    TIERED = "tiered"

    BILLING_SCHEME_TYPES = [
        (PER_UNIT, "Per Unit"),
        (TIERED, "Tiered"),
    ]

    active = models.BooleanField(
        help_text="Whether the price can be used for new purchases."
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=3,
        help_text=(
            "Three-letter ISO currency code, in lowercase. "
            "Must be a supported currency."
        ),
    )
    nickname = models.CharField(
        max_length=255,
        null=True,
        help_text="A brief description of the price, hidden from customers.",
    )
    recurring = models.JSONField(
        null=True,
        help_text=(
            "The recurring components of a price " "such as interval and usage_type."
        ),
    )

    type = models.CharField(
        choices=PRICE_TYPES,
        max_length=16,
        help_text=(
            "One of one_time or recurring depending on whether the price is for "
            "a one-time purchase or a recurring (subscription) purchase."
        ),
    )
    custom_unit_amount = models.JSONField(
        null=True,
        help_text=(
            "When set, provides configuration for the amount to be adjusted "
            "by the customer during Checkout Sessions and Payment Links."
        ),
    )
    unit_amount = models.BigIntegerField(
        null=True,
        help_text=(
            "The unit amount in cents to be charged, represented as a whole "
            "integer if possible. Null if a sub-cent precision is required"
        ),
    )
    unit_amount_decimal = models.DecimalField(
        null=True,
        max_digits=19,
        decimal_places=12,
        help_text=(
            "The unit amount in cents to be charged, represented as a decimal "
            "string with at most 12 decimal places"
        ),
    )
    billing_scheme = models.CharField(
        choices=BILLING_SCHEME_TYPES,
        max_length=16,
        help_text=(
            "Describes how to compute the price per period. Either per_unit or tiered."
            "per_unit indicates that the fixed amount "
            "(specified in unit_amount or unit_amount_decimal)"
            "will be charged per unit in quantity "
            "(for prices with usage_type=licensed),"
            "or per unit of total usage (for prices with usage_type=metered). "
            "Tiered indicates that the unit"
            "pricing will be computed using a tiering strategy "
            "as defined using the tiers and tiers_mode attributes."
        ),
    )

    tax_behavior = models.CharField(
        choices=TAX_BEHAVIOR_TYPES,
        max_length=16,
        help_text=(
            "Specifies whether the price is considered "
            "inclusive of taxes or exclusive of taxes."
            "One of inclusive, exclusive, or unspecified. "
            "Once specified as either inclusive or exclusive, it cannot be changed."
        ),
    )
    tiers = models.JSONField(
        null=True,
        help_text=(
            "Each element represents a pricing tier. "
            "This parameter requires billing_scheme to be set to tiered."
            "See also the documentation for billing_scheme. "
            "This field is not included by default."
            "To include it in the response, expand the tiers field."
        ),
    )
    tiers_mode = models.CharField(
        null=True,
        max_length=32,
        help_text=(
            "Defines if the tiering price should be graduated or volume based."
            "In volume-based tiering, the maximum quantity "
            "within a period determines the per unit price."
            "In graduated tiering, pricing can change as the quantity grows."
        ),
    )
    transform_quantity = models.JSONField(
        null=True,
        help_text=(
            "Apply a transformation to the reported usage or "
            "set quantity before computing the amount billed. "
            "Cannot be combined with tiers."
        ),
    )
    lookup_key = models.CharField(
        null=True,
        max_length=255,
        help_text=(
            "A lookup key used to retrieve prices dynamically from a static string. "
            "This may be up to 200 characters."
        ),
    )
    created = models.BigIntegerField(
        help_text=(
            "Time at which the object was created."
            "Measured in seconds since the Unix epoch"
        )
    )

    class Meta:
        abstract = True


class StripeBaseCoupon(StripeBaseModel):
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
        choices=CURRENCY_CHOICES,
        default=DEFAULT_CURRENCY,
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
    percent_off = models.PositiveIntegerField(
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
