import csv
from django.core.management.base import BaseCommand 
from strategies.utils import STRATEGIES
from trading_models.models import TradingModel 
from trading_models.utils import ML_MODELS


class Command(BaseCommand): 
    help = 'Add trading models for S&P 500'

    def handle(self, *args, **kwargs):
        optimal_parameters = {}
        training_percent = 0.3
        period = "10y"

        file_name = "trading_models/management/commands/sp500.csv"
        with open(file_name) as csvfile:
            stock_reader = csv.reader(csvfile, delimiter=',')
            # Ignore Header
            stock_reader.__next__()
            for stock_line in stock_reader:
                symbol = stock_line[0]
                for strategy in STRATEGIES.keys():
                    for ml_model in ML_MODELS.keys():
                        # If this symbol/strategy/ml_model does not exist
                        if 0 == TradingModel.objects.filter(symbol=symbol, strategy=strategy, ml_model=ml_model).count():
                            print(f"{symbol} {strategy} {ml_model}")
                            trading_model = TradingModel(
                                symbol=symbol,
                                strategy=strategy,
                                ml_model=ml_model,
                                optimal_parameters=optimal_parameters,
                                training_percent=training_percent,
                                period=period,
                            )
                            trading_model.save()
