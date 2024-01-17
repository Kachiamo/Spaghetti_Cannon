from django.core.management.base import BaseCommand 
from trading_models.models import TradingModel 
from trading_models.utils import train_trading_model


class Command(BaseCommand): 
    help = 'Train trading models that have not been trained yet'

    def handle(self, *args, **kwargs):
        trading_models = TradingModel.objects.filter(accuracy__isnull=True, skip=False)
        print(f"{len(trading_models)} untrained models")
        for trading_model in trading_models:
            print(trading_model)
            try:
                train_trading_model(trading_model)
            except Exception:
                print(f"{trading_model} failed")
                trading_model.skip = True
                trading_model.save()
