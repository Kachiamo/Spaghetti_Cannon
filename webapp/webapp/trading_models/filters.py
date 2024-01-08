from django_filters import rest_framework as filters

from .models import TradingModel


class TradingModelFilter(filters.FilterSet):
    class Meta:
        model = TradingModel
        fields = ['symbol', 'strategy', 'ml_model', 'period']
