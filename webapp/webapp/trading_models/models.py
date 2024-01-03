import uuid
from django.db import models


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
    strategy_settings = models.JSONField()
    ml_model = models.CharField(max_length=255)
    ml_model_settings = models.JSONField()
    training_start_date = models.DateField()
    training_end_date = models.DateField()
    # Outcome
    accuracy = models.FloatField(null=True, blank=True)
    precision_buy = models.FloatField(null=True, blank=True)
    recall_buy = models.FloatField(null=True, blank=True)
    precision_sell = models.FloatField(null=True, blank=True)
    recall_sell = models.FloatField(null=True, blank=True)
    precision_hold = models.FloatField(null=True, blank=True)
    recall_hold = models.FloatField(null=True, blank=True)