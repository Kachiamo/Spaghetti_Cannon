from django_filters import rest_framework as drf_filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from .import serializers, models, filters


class Stocks(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.Stock
    queryset = models.Stock.objects.all()
    filterset_class = filters.StockFilter
    filter_backends = (drf_filters.DjangoFilterBackend, OrderingFilter, )
    ordering_fields = ['symbol', 'name', 'country', 'ipo_year', 'sector', 'industry']
