from rest_framework import serializers


class StrategySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    features = serializers.ListField(child=serializers.CharField(max_length=200), max_length=200)
