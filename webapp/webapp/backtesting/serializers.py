import datetime
from rest_framework import serializers
from strategies.utils import STRATEGY_CHOICES
from .utils import PERIOD_CHOICES, SYMBOL_CHOICES


class BacktestingSerializer(serializers.Serializer):
    strategy_id = serializers.ChoiceField(choices=STRATEGY_CHOICES)
    symbol = serializers.ChoiceField(choices=SYMBOL_CHOICES)
    period = serializers.ChoiceField(choices=PERIOD_CHOICES)
