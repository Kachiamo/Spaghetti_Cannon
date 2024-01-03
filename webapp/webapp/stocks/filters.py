from django_filters import rest_framework as filters

from .models import Stock

class StockFilter(filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['symbol', 'country', 'ipo_year', 'sector']
