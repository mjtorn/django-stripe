# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel
from django_stripe.utils import Currency

CHARGE_AUTOMATICALLY = "charge_automatically"
SEND_INVOICE = "send_invoice"

INVOICE_COLLECTION_METHOD_TYPES = (
    (CHARGE_AUTOMATICALLY, "Charge Automatically"),
    (SEND_INVOICE, "Send_Invoice"),
)


class AbstractStripeSubscription(AbstractStripeModel):
    """
    Subscriptions allow us to charge a customer on a recurring basis.
    Stripe documentation: https://stripe.com/docs/api/subscriptions
    """

    # https://stripe.com/docs/api/subscriptions/object#subscription_object-status
    INCOMPLETE = "incomplete"  # if the initial payment attempt fails

    # If the first invoice is not paid within 23 hours
    # (Its a terminal status)
    INCOMPLETE_EXPIRED = "incomplete_expired"

    TRIALING = "trialing"
    ACTIVE = "active"
    # It becomes past_due when payment to renew it fails
    PAST_DUE = "past_due"

    # 1. It becomes canceled when failed payment is not paid
    #    after all retries / by the due date
    # 2. Can be cancelled manually (its a terminal status)
    CANCELED = "canceled"

    # It becomes unpaid when failed payment
    # is not paid after all retries / by the due date
    UNPAID = "unpaid"

    STATUS_CURRENT = [TRIALING, ACTIVE]
    STATUS_CANCELLED = [CANCELED, UNPAID]

    SUBSCRIPTION_STATUS_TYPES = (
        (INCOMPLETE, "Incomplete"),
        (INCOMPLETE_EXPIRED, "Incomplete Expired"),
        (TRIALING, "Trialing"),
        (ACTIVE, "Active"),
        (PAST_DUE, "Past Due"),
        (CANCELED, "Canceled"),
        (UNPAID, "Unpaid"),
    )

    items = models.JSONField(
        null=True,
        blank=True,
        help_text="List of subscription items, each with an attached price.",
    )
    application_fee_percent = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        help_text=(
            "A positive decimal that represents the fee percentage of the "
            "subscription invoice amount that will be transferred to the application "
            "owner's Stripe account each billing period."
        ),
    )
    automatic_tax = models.JSONField(
        null=True,
        blank=True,
        help_text="Automatic tax settings for this subscription.",
    )
    billing_cycle_anchor = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Determines the date of the first full invoice, and, for plans "
            "with `month` or `year` intervals, the day of the month for subsequent "
            "invoices"
        ),
    )
    billing_thresholds = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Define thresholds at which an invoice will be sent, "
            "and the subscription advanced to a new billing period"
        ),
    )
    cancel_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "A date in the future at which the subscription will automatically "
            "get canceled"
        ),
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text=(
            "If the subscription has been canceled with the ``at_period_end`` "
            "flag set to true, ``cancel_at_period_end`` "
            "on the subscription will be true. "
            "We can use this attribute to determine whether a subscription that has a "
            "status of active is scheduled to be canceled at the end of the "
            "current period"
        ),
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "If the subscription has been canceled, the date of that cancellation. "
            "If the subscription was canceled with ``cancel_at_period_end``, "
            "canceled_at will still reflect the date "
            "of the initial cancellation request, "
            "not the end of the subscription period "
            "when the subscription is automatically "
            "moved to a canceled state"
        ),
    )
    cancellation_details = models.JSONField(
        null=True,
        blank=True,
        help_text=("Details about why this subscription was cancelled"),
    )
    collection_method = models.CharField(
        choices=INVOICE_COLLECTION_METHOD_TYPES,
        max_length=32,
        help_text=(
            "Either `charge_automatically`, or `send_invoice`. "
            "When charging automatically, "
            "Stripe will attempt to pay this subscription "
            "at the end of the cycle using "
            "the default source attached to the customer. "
            "When sending an invoice, Stripe will email us customer an invoice with "
            "payment instructions"
        ),
    )
    current_period_end = models.DateTimeField(
        help_text="End of the current period for which the subscription has been "
        "invoiced. At the end of this period, a new invoice will be created"
    )
    current_period_start = models.DateTimeField(
        help_text=(
            "Start of the current period for which the subscription has "
            "been invoiced"
        )
    )
    days_until_due = models.IntegerField(
        null=True,
        blank=True,
        help_text=(
            "Number of days a customer has to pay invoices generated by this "
            "subscription. This value will be `null` for subscriptions where "
            "`billing=charge_automatically`"
        ),
    )
    default_payment_method = models.TextField(blank=True)
    default_source = models.TextField(blank=True)

    default_tax_rates = models.JSONField(null=True, blank=True)
    discount = models.JSONField(null=True, blank=True)
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "If the subscription has ended (either because it was canceled or "
            "because the customer was switched to a subscription to a new plan), "
            "the date the subscription ended"
        ),
    )
    next_pending_invoice_item_invoice = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Specifies the approximate timestamp on which any pending "
            "invoice items will be billed according to the schedule provided at "
            "pending_invoice_item_interval"
        ),
    )
    pause_collection = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "If specified, payment collection for this subscription will be paused."
        ),
    )
    pending_invoice_item_interval = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Specifies an interval for how often to bill for any "
            "pending invoice items. It is analogous to calling Create an invoice "
            "for the given subscription at the specified interval"
        ),
    )
    pending_setup_intent = models.TextField(blank=True)
    pending_update = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "If specified, pending updates that will be applied to the "
            "subscription once the latest_invoice has been paid"
        ),
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
        help_text=(
            "The quantity applied to this subscription. This value will be "
            "`null` for multi-plan subscriptions"
        ),
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Date when the subscription was first created. The date "
            "might differ from the created date due to backdating"
        ),
    )
    status = models.CharField(
        choices=SUBSCRIPTION_STATUS_TYPES,
        max_length=32,
        help_text="The status of this subscription",
    )

    # tax rate
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has a trial, the end of that trial",
    )
    trial_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If the subscription has a trial, the beginning of that trial",
    )
    trial_settings = models.JSONField(
        null=True,
        blank=True,
        help_text="Settings related to subscription trials.",
    )
    latest_invoice = models.CharField(
        max_length=255,
        blank=True,
        help_text="The most recent invoice this subscription has generated.",
    )
    currency = models.CharField(
        choices=Currency.choices,
        default=Currency.USD.value,
        max_length=3,
        help_text=(
            "The currency the customer can be charged "
            "in for recurring billing purposes"
        ),
    )

    class Meta:
        abstract = True
