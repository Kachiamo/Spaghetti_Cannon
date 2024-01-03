from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import STRATEGIES

from .import serializers


class Strategies(APIView):
    permission_classes = []
    authentication_classes = []

    serializer_class = serializers.StrategySerializer

    def get(self, request):
        serializer = serializers.StrategySerializer(STRATEGIES.values(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)
