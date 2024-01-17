import uuid
from django.db import models


def max_period():
    return "max"


def default_training_percent():
    return 0.3


class TradingModel(models.Model):
    class Meta:
        verbose_name = "Trading Model"
        verbose_name_plural = "Trading Models"

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # Settings
    symbol = models.CharField(max_length=255)
    strategy = models.CharField(max_length=255)
    ml_model = models.CharField(max_length=255)
    training_percent = models.FloatField(default=default_training_percent)
    period = models.CharField(default=max_period, max_length=3)
    skip = models.BooleanField(default=False)

    # Returns
    symbol_returns = models.FloatField(null=True, blank=True)
    strategy_returns = models.FloatField(null=True, blank=True)
    model_returns = models.FloatField(null=True, blank=True)

    # Outcome
    optimal_parameters = models.JSONField()
    accuracy = models.FloatField(null=True, blank=True)
    precision_buy = models.FloatField(null=True, blank=True)
    recall_buy = models.FloatField(null=True, blank=True)
    precision_sell = models.FloatField(null=True, blank=True)
    recall_sell = models.FloatField(null=True, blank=True)
    precision_hold = models.FloatField(null=True, blank=True)
    recall_hold = models.FloatField(null=True, blank=True)