from django_filters import rest_framework as filters

from .models import TradingModel


def filter_not_empty(queryset, name, value):
    lookup = '__'.join([name, 'isnull'])
    return queryset.filter(**{lookup: not value})


class TradingModelFilter(filters.FilterSet):
    trained = filters.BooleanFilter(field_name='accuracy', method=filter_not_empty)

    class Meta:
        model = TradingModel
        fields = ['symbol', 'strategy', 'ml_model', 'period', 'model_returns', 'skip']
