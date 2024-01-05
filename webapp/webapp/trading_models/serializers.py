from rest_framework import serializers

from stocks.utils import symbol_choices
from strategies.utils import STRATEGY_CHOICES
from .import models


class TradingModel(serializers.ModelSerializer):
    symbol = serializers.ChoiceField(choices=symbol_choices())
    strategy = serializers.ChoiceField(choices=STRATEGY_CHOICES)

    class Meta:
        model = models.TradingModel
        fields = '__all__'
