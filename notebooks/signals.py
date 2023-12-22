import pandas as pd
import numpy as np
import hvplot.pandas

COLOR_BUY = "green"
COLOR_SELL = "red"
SYMBOL_SELL = "v"
SYMBOL_BUY = "^"


class TradingStrategy():
    strategy = "Strategy Abbreviation"
    df = None
    ticker = None

    def add_signals(self):
        pass

    def plot(self):
        exit = self.df[self.df[f"{self.strategy}_Action"] == -1.0]["Close"].hvplot.scatter(
            color=COLOR_SELL,
            marker=SYMBOL_SELL,
            size=200,
            legend=False,
            ylabel="Price in $",
            width=1000,
            height=400
        )
        entry = self.df[self.df[f"{self.strategy}_Action"] == 1.0]["Close"].hvplot.scatter(
            color=COLOR_BUY,
            marker=SYMBOL_BUY,
            size=200,
            legend=False,
            ylabel="Price in $",
            width=1000,
            height=400
        )
        close = self.df[["Close"]].hvplot(
            line_color="lightgray",
            ylabel="Price in $",
            width=1000,
            height=400
        )

        combined_plot = close * entry * exit

        combined_plot.opts(
            title=f"{self.ticker} - {self.strategy}, Entry and Exit Points"
        )
        return combined_plot


class BuyHoldTradingStrategy(TradingStrategy):
    strategy = "BuyHold"

    def __init__(self, *args, **kwargs):
        super(BuyHoldTradingStrategy, self).__init__()
        self.df = args[0]
        self.ticker = kwargs.get("ticker")
        self.add_signals()

    def add_signals(self):
        self.df[f"{self.strategy}_Signal"] = 1.0
        self.df[f"{self.strategy}_Action"] = self.df[f"{self.strategy}_Signal"].diff()
        self.df[f"{self.strategy}_Action"][0] = 1.0


class SMATradingStrategy(TradingStrategy):
    strategy = "SMA"

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
        self.df[f"{self.strategy}_Signal"][self.short_window:] = np.where(
            self.df[self.short_window_column][self.short_window:] > self.df[self.long_window_column][self.short_window:], 1.0, 0.0
        )
        self.df[f"{self.strategy}_Action"] = self.df[f"{self.strategy}_Signal"].diff()

    def plot(self):
        moving_avgs = self.df[[self.short_window_column, self.long_window_column]].hvplot(
            ylabel="Price in $",
            width=1000,
            height=400
        )

        combined_plot = moving_avgs * super(SMATradingStrategy, self).plot()

        combined_plot.opts(
            title=f"{self.ticker} - {self.strategy}, Entry and Exit Points"
        )
        return combined_plot
