import datetime
from rest_framework import serializers
from strategies.utils import STRATEGY_CHOICES
from stocks.utils import symbol_choices
from .utils import PERIOD_CHOICES


class BacktestingSerializer(serializers.Serializer):
    strategy_id = serializers.ChoiceField(choices=STRATEGY_CHOICES)
    symbol = serializers.ChoiceField(choices=symbol_choices())
    period = serializers.ChoiceField(choices=PERIOD_CHOICES)
