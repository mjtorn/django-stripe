# Django Stripe Stuff
from django_stripe.actions import StripeCouponAction
from django_stripe.webhooks.register import StripeWebhook


class CouponStripeWebhook(StripeWebhook):
    def process_webhook(self):
        if self.event.validated_message:
            StripeCouponAction().sync(
                self.event.validated_message["data"]["object"].copy()
            )


class CouponCreatedWebhook(CouponStripeWebhook):
    name = "coupon.created"
    description = "Occurs whenever a new coupon is created."


class CouponUpdatedWebhook(CouponStripeWebhook):
    name = "coupon.updated"
    description = "Occurs whenever any property of a coupon changes."


class CouponDeletedWebhook(CouponStripeWebhook):
    name = "coupon.deleted"
    description = "Occurs whenever a coupon is deleted."

    def process_webhook(self):
        StripeCouponAction().soft_delete(
            self.event.validated_message["data"]["object"]["id"]
        )
