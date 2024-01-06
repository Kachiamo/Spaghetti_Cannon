from rest_framework import serializers

from stocks.utils import symbol_choices
from strategies.utils import STRATEGY_CHOICES
from backtesting.utils import PERIOD_CHOICES
from .import models
from .utils import ML_MODEL_CHOICES


class TradingModel(serializers.ModelSerializer):
    symbol = serializers.ChoiceField(choices=symbol_choices())
    strategy = serializers.ChoiceField(choices=STRATEGY_CHOICES)
    ml_model = serializers.ChoiceField(choices=ML_MODEL_CHOICES)
    period = serializers.ChoiceField(choices=PERIOD_CHOICES)
    training_percent = serializers.FloatField(min_value=0.1, max_value=0.5, default=0.3)

    class Meta:
        model = models.TradingModel
        fields = '__all__'

class TrainSerializer(serializers.Serializer):
    pass
