import logging
import os
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
from .models import Stock

logging.basicConfig()
log = logging.getLogger(__name__)

TAGS = [
    "s&p 500"
]

def symbol_choices():
    try:
        values = Stock.objects.values_list('symbol', 'name')
        # Include the symbol and name in the display
        ret = [(item[0], f"{item[0]}: {item[1]}") for item in values]
        return ret
    except Exception:
        return []


def get_history(symbol, period):
    history = None
    path = Path(f"./stock_data/{symbol.replace('/','_')}.csv")
    history = pd.read_csv(
        path,
        index_col='Date',
        parse_dates=True
    )
    if period != "max":
        if "mo" in period:
            period = period.replace("mo", "")
            start_date = datetime.utcnow().replace(tzinfo=pytz.utc) - relativedelta(months=int(period))
        if "y" in period:
            period = period.replace("y", "")
            start_date = datetime.utcnow().replace(tzinfo=pytz.utc) - relativedelta(years=int(period))
        return history[start_date:]
    return history


def update_history(symbol):
    '''
    If there is no existing stock data, download everything.  If not, download what is needed
    '''
    history = None
    path = Path(f"./stock_data/{symbol.replace('/','_')}.csv")
    log.critical(f"path {path}")
    ticker = yf.Ticker(symbol)
    if os.path.isfile(path):
        try:
            history = pd.read_csv(
                path,
                index_col='Date',
                parse_dates=True
            )
            last_index = history.index[-1]
            start_date = last_index + timedelta(days=1)
            end_date = datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(days=1)
            if start_date > end_date:
                return
            stock_data = ticker.history(start=start_date, end=end_date)
            history = pd.concat([history, stock_data])
        except Exception:
            log.exception(f"Failed to get history for {symbol}")
            pass

    if history is None:
        history = ticker.history(period="max")
    if history is not None:
        history.to_csv(path)
