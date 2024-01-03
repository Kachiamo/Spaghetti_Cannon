from rest_framework import serializers

from .import models


class Stock(serializers.ModelSerializer):

    class Meta:
        model = models.Stock
        fields = '__all__'
