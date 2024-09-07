from types import DynamicClassAttribute

from django.db.models import TextChoices


class Currency(TextChoices):
    USD = "usd"

    @DynamicClassAttribute
    def label(self):
        return self._label_.upper()
