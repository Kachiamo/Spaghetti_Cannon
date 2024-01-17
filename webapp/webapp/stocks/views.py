from django_filters import rest_framework as drf_filters
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .import serializers, models, filters, utils


class Stocks(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.Stock
    queryset = models.Stock.objects.all()
    filterset_class = filters.StockFilter
    filter_backends = (drf_filters.DjangoFilterBackend, OrderingFilter, )
    ordering_fields = ['symbol', 'name', 'country', 'ipo_year', 'sector', 'industry']


class UpdateStocks(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.Stock
    queryset = models.Stock.objects.all()
    filterset_class = filters.StockFilter
    filter_backends = (drf_filters.DjangoFilterBackend, OrderingFilter, )
    ordering_fields = ['symbol', 'name', 'country', 'ipo_year', 'sector', 'industry']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.Stock
        else:
            return serializers.UpdateHistorySerializer

    def create(self, request, *args, **kwargs):
        for stock in self.queryset.all():
            utils.update_history(stock.symbol)
        return Response(None, status.HTTP_200_OK)


class Stock(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.Stock
    queryset = models.Stock.objects.all()
    filterset_class = filters.StockFilter
    filter_backends = (drf_filters.DjangoFilterBackend, OrderingFilter, )
    ordering_fields = ['symbol', 'name', 'country', 'ipo_year', 'sector', 'industry']


class UpdateStock(generics.RetrieveUpdateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.Stock
    queryset = models.Stock.objects.all()
    filterset_class = filters.StockFilter
    filter_backends = (drf_filters.DjangoFilterBackend, OrderingFilter, )
    ordering_fields = ['symbol', 'name', 'country', 'ipo_year', 'sector', 'industry']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.Stock
        else:
            return serializers.UpdateHistorySerializer

    def update(self, request, *args, **kwargs):
        stock = self.get_object()
        utils.update_history(stock.symbol)
        return Response(None, status.HTTP_200_OK)