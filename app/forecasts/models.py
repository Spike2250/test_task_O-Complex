from django.db import models
from django.utils.translation import gettext as _

from ..users.models import User


class Forecast(models.Model):
    place = models.CharField(
        max_length=255, unique=False, blank=False,
        verbose_name=_('Place'),
    )
    forecast_today = models.JSONField(
        blank=True,
        verbose_name=_('Forecast Today'),
    )
    forecast_tomorrow = models.JSONField(
        blank=True,
        verbose_name=_('Forecast Tomorrow'),
    )
    author = models.ForeignKey(
        User, blank=False, on_delete=models.CASCADE,
        related_name='author',
        verbose_name=_('Author'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
