from rest_framework import serializers
from strategies.utils import STRATEGY_CHOICES
from backtesting.utils import PERIOD_CHOICES


class ActionSerializer(serializers.Serializer):
    strategy_id = serializers.ChoiceField(choices=STRATEGY_CHOICES)
    period = serializers.ChoiceField(choices=PERIOD_CHOICES)
    max_position = serializers.IntegerField()
    buy = serializers.BooleanField(default=True)
    sell = serializers.BooleanField(default=True)
    hold = serializers.BooleanField(default=True)
    tag = serializers.CharField(required=False)
    symbols = serializers.ListField(child=serializers.CharField(), required=False)
