from bokeh.embed import components
from bokeh.plotting import figure
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .import serializers, models


class TradingModels(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.TradingModel
    queryset = models.TradingModel.objects.all()


class TradingModel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.TradingModel
    queryset = models.TradingModel.objects.all()


class TrainTradingModel(generics.UpdateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.TradingModel
    queryset = models.TradingModel.objects.all()