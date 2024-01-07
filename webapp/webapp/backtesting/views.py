from bokeh.embed import components
from bokeh.plotting import figure
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .import serializers
from .utils import backtest


class Backtest(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []

    serializer_class = serializers.BacktestingSerializer

    def get(self, request):
        return Response(None, status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Get the trading strategy to backtest
        strategy = backtest(data["strategy_id"], data["symbol"], data["period"])

        # Get the bokeh components to render
        strategy_script, strategy_div = components(strategy.plot())
        returns_script, returns_div = components(strategy.plot_returns())
        kwargs = {
            "strategy": strategy,
            "plots": {
                "strategy": {
                    "script": strategy_script,
                    "div": strategy_div,
                },
                "returns": {
                    "script": returns_script,
                    "div": returns_div,
                }
            }
        }
    
        return render(request, 'base.html', context=kwargs)
