import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from stocks.models import Stock
from .import serializers
from backtesting.utils import backtest

logging.basicConfig()
log = logging.getLogger(__name__)


class Action(APIView):
    permission_classes = []
    authentication_classes = []

    serializer_class = serializers.ActionSerializer

    def get(self, request):
        return Response(None, status.HTTP_200_OK)
    
    def post(self, request):
        actions = []
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        buy = data["buy"]
        sell = data["sell"]
        hold = data["hold"]
        tag = data.get("tag")
        symbols = data.get("symbols")

        stocks = Stock.objects
        if tag and len(tag) > 0:
            stocks = stocks.filter(tags__contains=tag)
        if symbols and len(symbols) > 0:
            stocks = stocks.filter(symbol__in=symbols)
        for stock in stocks:
            log.critical(stock.symbol)
            # Get the trading strategy to backtest
            try:
                strategy = backtest(data["strategy_id"], stock.symbol, data["period"])
                strategy.add_position_and_returns(max_position=data["max_position"])
                action = strategy.get_action()
                strategy_returns = strategy.df.iloc[-1]["Strategy_Cumulative_Returns"]
                stock_returns = strategy.df.iloc[-1]["Stock_Cumulative_Returns"]
                # No penny stocks
                low = strategy.df["Low"].max()
                if (action == 1 and buy and strategy_returns > 1 and stock_returns > 1 and strategy_returns > stock_returns and low > 1) or (action == 0 and hold) or (action == -1 and sell):
                    outcome = {
                        "symbol": stock.symbol,
                        "action": action,
                        "strategy_returns": strategy_returns,
                        "stock_returns": stock_returns
                    }
                    log.critical(outcome)
                    actions.append(outcome)
            except Exception:
                pass
        return Response(actions, status.HTTP_200_OK)
