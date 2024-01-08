from django.core.management.base import BaseCommand 
from trading_models.models import TradingModel 
from trading_models.utils import train_trading_model


class Command(BaseCommand): 
    help = 'Train trading models that have not been trained yet'

    def handle(self, *args, **kwargs):
        trading_models = TradingModel.objects.filter(accuracy__isnull=True)[0:10]
        for trading_model in trading_models:
            print(trading_model)
            train_trading_model(trading_model)
