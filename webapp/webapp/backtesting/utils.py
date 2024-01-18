import logging
from stocks.utils import get_history

from strategies.utils import STRATEGIES

logging.basicConfig()
log = logging.getLogger(__name__)


PERIOD_CHOICES = {
    "1mo": "1mo",
    "3mo": "3mo",
    "6mo": "6mo",
    "1y": "1y",
    "2y": "2y",
    "5y": "5y",
    "10y": "10y",
    "max": "max",
}


def backtest(strategy_id, symbol, period):
    strategy_class = STRATEGIES[strategy_id]
    history = get_history(symbol, period=period)
    return strategy_class(history, ticker=symbol)
