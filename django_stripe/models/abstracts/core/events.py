# Third Party Stuff
from django.db import models

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel


class AbstractStripeEvent(AbstractStripeModel):
    kind = models.CharField(max_length=255)
    webhook_message = models.JSONField()
    validated_message = models.JSONField(null=True, blank=True)
    valid = models.BooleanField(null=True)
    processed = models.BooleanField(default=False)
    request = models.JSONField(
        null=True,
        help_text=(
            "Information on the API request that instigated the event, "
            "If null, the event was automatic"
            " (e.g., Stripe’s automatic subscription handling)"
        ),
    )
    pending_webhooks = models.PositiveIntegerField(
        default=0,
        help_text=(
            "Number of webhooks that have yet to be successfully "
            "delivered (i.e., to return a 20x response) "
            "to the URLs we’ve specified"
        ),
    )
    api_version = models.CharField(max_length=128, blank=True)

    @property
    def message(self):
        return self.validated_message

    def __str__(self):
        return "{} - {}".format(self.kind, self.stripe_id)

    class Meta:
        abstract = True
