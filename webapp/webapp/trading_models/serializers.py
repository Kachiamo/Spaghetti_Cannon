from rest_framework import serializers

from .import models


class TradingModel(serializers.ModelSerializer):
    class Meta:
        model = models.TradingModel
        fields = '__all__'
