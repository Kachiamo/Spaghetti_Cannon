import logging
import pandas as pd
import numpy as np
import hvplot.pandas
from bokeh.plotting import figure
from bokeh.palettes import Category20b

COLOR_BUY = "green"
COLOR_SELL = "red"
SYMBOL_SELL = "v"
SYMBOL_BUY = "^"

logging.basicConfig()
log = logging.getLogger(__name__)


def add_year_day(df):
    '''
    Utility function to add the day of the year to the dataframe
    '''
    df['Year_Day'] = [dt.timetuple().tm_yday for dt in df.index.to_pydatetime()]


class TradingStrategy():
    strategy = "Strategy Abbreviation"
    df = None
    ticker = None

    def add_signals(self):
        pass

    def plot(self):
        plot = figure(x_range=(self.df.index[0], self.df.index[-1]), frame_width=1024, frame_height=768)
        plot.line(
            x=self.df.index,
            y=self.df[["Close"]],
            legend_label=self.ticker,
        )
        plot.triangle(
            self.df[self.df[f"{self.strategy}_Action"] == 1.0].index,
            self.df[self.df[f"{self.strategy}_Action"] == 1.0]["Close"],
            color=COLOR_BUY,
            size=20,
        )
        plot.inverted_triangle(
            self.df[self.df[f"{self.strategy}_Action"] == -1.0].index,
            self.df[self.df[f"{self.strategy}_Action"] == -1.0]["Close"],
            color=COLOR_SELL,
            size=20,
        )
        return plot


class BuyHoldTradingStrategy(TradingStrategy):
    id = "bh"
    name = "Buy and Hold"
    strategy = "BuyHold"
    features = []

    def __init__(self, *args, **kwargs):
        super(BuyHoldTradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.add_signals()

    def add_signals(self):
        self.df[f"{self.strategy}_Signal"] = 1.0
        self.df[f"{self.strategy}_Action"] = self.df[f"{self.strategy}_Signal"].diff()
        self.df.loc[self.df.index[0], f"{self.strategy}_Action"] = 1.0


class DCATradingStrategy(TradingStrategy):
    id = "dca"
    name = "Dollar Cost Average"
    strategy = "DCA"
    features = ["year_day"]

    def __init__(self, *args, **kwargs):
        super(DCATradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.contributions_per_year = kwargs.get("contributions_per_year", 12)
        self.add_signals()

    def add_signals(self):
        self.df[f"{self.strategy}_Signal"] = 1.0
        self.df[f"{self.strategy}_Action"] = 0.0

        # The period is the number of days between contributions
        period = round(252/self.contributions_per_year)

        # Get date range
        start_year = self.df.index.date[0].year
        end_year = self.df.index.date[-1].year

        # There might be a more elegant way to pull this off without a for and while loop
        # Just can't think of it at the moment.
        # Might involve using the datetime.timetuple().tm_yday
        # This might also be needed for the ML model to properly train using day of year
        for year in range(start_year, end_year + 1):
            # Get a dataframe for each year
            df_for_year = self.df[self.df.index.year == year]
            i = 0
            # Walk through each period for the year
            # and set the buy signal
            while i < len(df_for_year[f"{self.strategy}_Action"]):
                dt = df_for_year.index[i]
                self.df.loc[dt, f"{self.strategy}_Action"] = 1.0
                i += period


class SMATradingStrategy(TradingStrategy):
    id = "sma"
    name = "Simple Moving Average"
    strategy = "SMA"
    features = ["Close", "short_window", "long_window"]

    def __init__(self, *args, **kwargs):
        super(SMATradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.short_window = kwargs.get("short_window", 50)
        self.long_window = kwargs.get("long_window", 100)
        self.short_window_column = f"{self.strategy}_{self.short_window}"
        self.long_window_column = f"{self.strategy}_{self.long_window}"
        self.add_signals()

    def add_signals(self):
        self.df[self.short_window_column] = self.df["Close"].rolling(window=self.short_window).mean()
        self.df[self.long_window_column] = self.df["Close"].rolling(window=self.long_window).mean()
        self.df[f"{self.strategy}_Signal"] = 0.0
        dt = self.df.index[self.short_window]
        self.df.loc[dt:, f"{self.strategy}_Signal"] = np.where(
            self.df[self.short_window_column][self.short_window:] > self.df[self.long_window_column][self.short_window:], 1.0, 0.0
        )
        self.df[f"{self.strategy}_Action"] = self.df[f"{self.strategy}_Signal"].diff()

    def plot(self):
        plot = super(SMATradingStrategy, self).plot()
        plot.line(
            x=self.df.index,
            y=self.df[[self.short_window_column]],
            legend_label="Short Window",
        )
        plot.line(
            x=self.df.index,
            y=self.df[[self.long_window_column]],
            legend_label="Long Window",
        )
        return plot


class RSITradingStrategy(TradingStrategy):
    id = "rsi"
    name = "Relative Strength Index"
    strategy = "RSI"
    features = [
        "Close",
        "Positive_Returns",
        "Negative_Returns",
        "Positive_RS",
        "Negative_RS",
    ]

    def __init__(self, *args, **kwargs):
        super(RSITradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.window = kwargs.get("window", 14)
        self.over_sold = kwargs.get("over_sold", 70)
        self.under_sold = kwargs.get("under_sold", 30)
        self.add_signals()

    def add_signals(self):
        self.df["Returns"] = self.df["Close"].pct_change()
        # Create a column for positive returns
        self.df["Positive_Returns"] = np.where(
            self.df["Returns"] > 0, self.df["Returns"], 0.0
        )
        # Create a column for negative returns
        self.df["Negative_Returns"] = np.where(
            self.df["Returns"] < 0, self.df["Returns"], 0.0
        )
        # Create columns for positive and negative RS
        self.df["Positive_RS"] = (self.df["Positive_Returns"].rolling(window=self.window).sum())/self.window
        self.df["Negative_RS"] = (self.df["Negative_Returns"].rolling(window=self.window).sum())/(-self.window)

        self.df[f"{self.strategy}_Signal"] = 100 - (100 / (1 + (self.df["Positive_RS"]/self.df["Negative_RS"])))
        self.df[f"{self.strategy}_Action"] = np.where(
            self.df[f"{self.strategy}_Signal"] >= self.over_sold, -1, np.where(
                self.df[f"{self.strategy}_Signal"] <= self.under_sold, 1, 0
            )
        )


class ATRTradingStrategy(TradingStrategy):
    id = "atr"
    name = "Average True Range"
    strategy = "ATR"
    features = [
        "Close",
        "TR",
        "ATR",
    ]

    def __init__(self, *args, **kwargs):
        super(ATRTradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.window = kwargs.get("window", 14)
        self.atr_multiplier = kwargs.get("atr_multiplier", 1.5)
        self.add_signals()

    def add_signals(self):
        self.df["Returns"] = self.df["Close"].pct_change()
        # Create a column for positive returns
        self.df["TR"] = self.df.apply(lambda row: max(row['High'] - row['Low'], abs(row['High'] - row['Close']), abs(row['Low'] - row['Close'])), axis=1)
        self.df['ATR'] = self.df['TR'].rolling(window=self.window).mean()

        self.df[f"{self.strategy}_Action"] = np.where(
            self.df['Close'] - self.atr_multiplier * self.df['ATR'] > self.df['Close'].shift(1), 1.0, np.where(
                self.df['Close'] + self.atr_multiplier * self.df['ATR'] < self.df['Close'].shift(1), -1.0, 0.0
            )
        )


class StochasticOscillatorTradingStrategy(TradingStrategy):
    id = "stoch"
    name = "Stochastic Oscillator"
    strategy = "SO"
    features = [
        "Close",
        "%K",
        "%D",
        "Long Signal",
        "Short Signal",
        "Low",
        "High",
    ]

    def __init__(self, *args, **kwargs):
        super(StochasticOscillatorTradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.k_period = kwargs.get("k_period", 14)
        self.d_period = kwargs.get("d_period", 3)
        self.overbought = kwargs.get("overbought", 80)
        self.oversold = kwargs.get("overbought", 20)
        self.add_signals()

    def add_signals(self):
        self.df['%K'] = 100 * ((self.df['Close'] - self.df['Low'].rolling(window=self.k_period).min()) / (self.df['High'].rolling(window=self.k_period).max() - self.df['Low'].rolling(window=self.k_period).min()))
        self.df['%D'] = self.df['%K'].rolling(window=self.d_period).mean()
        self.df['Long Signal'] = (self.df['%K'] < self.oversold) & (self.df['%D'] < self.oversold)
        self.df['Short Signal'] = (self.df['%K'] > self.overbought) & (self.df['%D'] > self.overbought)
        self.df[f"{self.strategy}_Action"] = np.where(
            self.df['Short Signal'], -1, np.where(
                self.df['Long Signal'], 1, 0
            )
        )

    
class MovingAverageConvergenceDivergenceTradingStrategy(TradingStrategy):
    id = "macd"
    name = "Moving Average Convergence Divergence"
    strategy = "MACD"
    features = [
        "Close",
        "Short EMA",
        "Long EMA",
        "Long Signal",
        "Short Signal",
        "Signal Line",
        "MACD Hisotgram",
    ]

    def __init__(self, *args, **kwargs):
        super(MovingAverageConvergenceDivergence, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.short_window = kwargs.get("short_window", 12)
        self.long_window = kwargs.get("long_window", 26)
        self.signal_window = kwargs.get("signal_window", 9)
        self.add_signals()

    def add_signals(self):
        self.df['Short_EMA'] = self.df['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.df['Long_EMA'] = self.df['Close'].ewm(span=self.long_window, adjust=False).mean()
        self.df['MACD'] = self.df['Short_EMA'] - self.df['Long_EMA']
        self.df['Signal_Line'] = self.df['MACD'].ewm(span=self.signal_window, adjust=False).mean()
        self.df['MACD_Histogram'] = self.df['MACD'] - self.df['Signal_Line']
        self.df['Long Signal'] = self.df['MACD'] > self.df['Signal_Line']
        self.df['Short Signal'] = self.df['MACD'] < self.df['Signal_Line']
        self.df[f"{self.strategy}_Action"] = np.where(
            self.df['Short Signal'], -1, np.where(
                self.df['Long Signal'], 1,0
            )
        )
        