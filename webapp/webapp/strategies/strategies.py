import logging
import sys
import math
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
    max_position = sys.maxsize

    def add_signals(self):
        pass

    def add_position_and_returns(self):
        # Compute Position
        self.df["Cash"] = 0.0
        self.df["{self.strategy}_Position"] = 0
        # Compute Position Returns
        current_position = 0
        current_cash = self.df.loc[self.df.index[0], "Close"]
        for index, row in self.df.iterrows():
            # Get the current action
            close = row["Close"]
            action = row[f"{self.strategy}_Action"]
            action = action if not math.isnan(action) else 0

            # Take the action if possible
            if action > 0:
                if action + current_position < self.max_position:
                    current_position += action
                    current_cash -= action*close
                else:
                    action = 0
            elif action < 0:
                if action + current_position >= 0:
                    current_position += action
                    current_cash += -action*close
                else:
                    action = 0

            # Update enabled and position
            self.df.loc[index, f"{self.strategy}_Enabled"] = min(current_position, 1)
            self.df.loc[index, f"{self.strategy}_Position"] = current_position
            self.df.loc[index, "Cash"] = current_cash

        # Compute Holdings
        self.df[f"{self.ticker}_Holdings"] = self.df["Close"] * self.df[f"{self.strategy}_Position"]

        # Compute Profit
        self.df["Daily_Stock_Value"] = self.df["Close"]
        self.df["Daily_Strategy_Value"] = self.df[f"{self.ticker}_Holdings"] + self.df["Cash"]

        # Compute Returns
        self.df["Daily_Stock_Returns"] = self.df["Daily_Stock_Value"].pct_change()
        self.df["Daily_Strategy_Returns"] = self.df["Daily_Strategy_Value"].pct_change()

        # Compute Cumulative Daily Returns
        self.df["Stock_Cumulative_Returns"] = (self.df["Daily_Stock_Returns"] + 1).cumprod()
        self.df["Strategy_Cumulative_Returns"] = (self.df["Daily_Strategy_Returns"] + 1).cumprod()


    def plot_returns(self):
        plot = figure(x_range=(self.df.index[0], self.df.index[-1]), frame_width=1024, frame_height=768)
        plot.line(
            x=self.df.index,
            y=self.df[["Stock_Cumulative_Returns"]],
            legend_label="Stock Cumulative Returns",
            color="blue",
        )
        plot.line(
            x=self.df.index,
            y=self.df[["Strategy_Cumulative_Returns"]],
            legend_label="Strategy Cumulative Returns",
            color=COLOR_BUY,
        )
        plot.line(
            x=self.df.index,
            y=self.df[[f"{self.strategy}_Position"]],
            legend_label="Strategy Position",
            color="black",
        )
        return plot
    
    def plot_holdings(self):
        plot = figure(x_range=(self.df.index[0], self.df.index[-1]), frame_width=1024, frame_height=768)
        plot.line(
            x=self.df.index,
            y=self.df[["Daily_Stock_Value"]],
            legend_label="Daily Stock Value",
            color="blue",
        )
        plot.line(
            x=self.df.index,
            y=self.df[["Daily_Strategy_Value"]],
            legend_label="Daily Strategy Value",
            color="green",
        )
        return plot

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
        self.add_position_and_returns()


class DCATradingStrategy(TradingStrategy):
    id = "dca"
    name = "Dollar Cost Average"
    strategy = "DCA"
    features = []

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
        self.add_position_and_returns()


class SMATradingStrategy(TradingStrategy):
    id = "sma"
    name = "Simple Moving Average"
    strategy = "SMA"
    features = ["SMA_Short_Window", "SMA_Long_Window"]

    def __init__(self, *args, **kwargs):
        super(SMATradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.short_window = kwargs.get("short_window", 50)
        self.long_window = kwargs.get("long_window", 100)
        self.add_signals()

    def add_signals(self):
        self.df["SMA_Short_Window"] = self.df["Close"].rolling(window=self.short_window).mean()
        self.df["SMA_Long_Window"] = self.df["Close"].rolling(window=self.long_window).mean()
        self.df["SMA_Signal"] = 0.0
        dt = self.df.index[self.short_window]
        self.df.loc[dt:, "SMA_Signal"] = np.where(
            self.df["SMA_Short_Window"][self.short_window:] > self.df["SMA_Long_Window"][self.short_window:], 1.0, 0.0
        )
        self.df["SMA_Action"] = self.df["SMA_Signal"].diff()
        self.add_position_and_returns()

    def plot(self):
        plot = super(SMATradingStrategy, self).plot()
        plot.line(
            x=self.df.index,
            y=self.df[["SMA_Short_Window"]],
            legend_label="Short Window",
        )
        plot.line(
            x=self.df.index,
            y=self.df[["SMA_Long_Window"]],
            legend_label="Long Window",
        )
        return plot


class RSITradingStrategy(TradingStrategy):
    id = "rsi"
    name = "Relative Strength Index"
    strategy = "RSI"
    features = [
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
        self.add_position_and_returns()


class ATRTradingStrategy(TradingStrategy):
    id = "atr"
    name = "Average True Range"
    strategy = "ATR"
    features = [
        "Close",
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
        self.add_position_and_returns()


class StochasticOscillatorTradingStrategy(TradingStrategy):
    id = "stoch"
    name = "Stochastic Oscillator"
    strategy = "SO"
    features = [
        "%K",
        "%D",
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
        self.add_position_and_returns()

    
class MovingAverageConvergenceDivergenceTradingStrategy(TradingStrategy):
    id = "macd"
    name = "Moving Average Convergence Divergence"
    strategy = "MACD"
    features = [
        "MACD",
        "Signal_Line",
    ]

    def __init__(self, *args, **kwargs):
        super(MovingAverageConvergenceDivergenceTradingStrategy, self).__init__()
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
                self.df['Long Signal'], 1, 0
            )
        )
        self.add_position_and_returns()


class BollingerBandsTradingStrategy(TradingStrategy):
    id = "bb"
    name = "Bollinger Bands"
    strategy = "BB"
    features = [
        "Close",
        "BB_UPPER",
        "BB_LOWER",
        "BB_MIDDLE",
    ]

    def __init__(self, *args, **kwargs):
        super(BollingerBandsTradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.window = kwargs.get("window", 40)
        self.std_devs = kwargs.get("std_devs", 2)
        self.add_signals()

    def add_signals(self):
        self.df['BB_MIDDLE'] = self.df['Close'].rolling(window=self.window).mean()
        self.df['BB_UPPER'] = self.df['BB_MIDDLE'] + (self.df['Close'].rolling(window=self.window).std() * self.std_devs)
        self.df['BB_LOWER'] = self.df['BB_MIDDLE'] - (self.df['Close'].rolling(window=self.window).std() * self.std_devs)
        self.df[f"{self.strategy}_Action"] = np.where(
            self.df['Close'] < self.df['BB_LOWER'], 1, np.where(
                self.df['Close'] > self.df['BB_UPPER'], -1, 0
            )
        )
    
        self.add_position_and_returns()
