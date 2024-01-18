import logging
import csv
from django.core.management.base import BaseCommand 
from stocks.models import Stock

logging.basicConfig()
log = logging.getLogger(__name__)


class Command(BaseCommand): 
    help = 'Add trading models for S&P 500'

    def handle(self, *args, **kwargs):
        optimal_parameters = {}
        training_percent = 0.3
        period = "1y"

        file_name = "stocks/management/commands/constituents.csv"
        with open(file_name) as csvfile:
            stock_reader = csv.reader(csvfile, delimiter=',')
            # Ignore Header
            stock_reader.__next__()
            for stock_line in stock_reader:
                symbol = stock_line[0]
                try:
                    stock = Stock.objects.get(symbol=symbol)
                    if "s&p 500" not in stock.tags:
                        stock.tags.append("s&p 500")
                        stock.save()
                except Exception:
                    log.exception(f"failed to tag {symbol}")
