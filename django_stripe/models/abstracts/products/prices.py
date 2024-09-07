# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel
from django_stripe.utils import Currency


class AbstractStripePrice(AbstractStripeModel):
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
        choices=Currency.choices,
        default=Currency.USD.value,
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
            "The recurring components of a price such as interval and usage_type."
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
