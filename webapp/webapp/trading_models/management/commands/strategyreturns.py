from django.core.management.base import BaseCommand 
from trading_models.models import TradingModel 
from trading_models.utils import backtest_strategy


class Command(BaseCommand): 
    help = 'Train trading models that have not been trained yet'

    def handle(self, *args, **kwargs):
        trading_models = TradingModel.objects.filter(strategy_returns__isnull=True)
        print(f"{len(trading_models)} strategies need backtesting")
        for trading_model in trading_models:
            print(trading_model)
            backtest_strategy(trading_model)
