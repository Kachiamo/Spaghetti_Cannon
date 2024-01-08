from bokeh.embed import components
from bokeh.plotting import figure
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters import rest_framework as drf_filters

from .utils import train_trading_model
from .import serializers, models, filters


class TradingModels(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.TradingModel
    queryset = models.TradingModel.objects.all()
    filterset_class = filters.TradingModelFilter
    filter_backends = (drf_filters.DjangoFilterBackend,)


class TradingModel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.TradingModel
    queryset = models.TradingModel.objects.all()


class TrainTradingModel(generics.RetrieveUpdateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = models.TradingModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TradingModel
        else:
            return serializers.TrainSerializer

    def update(self, request, *args, **kwargs):
        trading_model = self.get_object()
        train_trading_model(trading_model)
        return Response(None, status.HTTP_200_OK)
