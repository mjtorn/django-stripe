from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from django_stripe.actions import StripeWebhook


class StripeWebhookViewSet(viewsets.GenericViewSet):
    # Check the webhook signatures
    # Ref: https://stripe.com/docs/webhooks/signatures

    def create(self, request, *args, **kwargs):
        try:
            event_data = request.data
            StripeWebhook.process_webhook(event_data)
        except Http404 as e:
            raise e
        return Response({"success": True}, 200)
