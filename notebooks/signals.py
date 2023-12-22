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


class DCATradingStrategy(TradingStrategy):
    strategy = "DCA"

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
            while i < len(df_for_year["DCA_Action"]):
                dt = df_for_year.index[i]
                self.df.loc[dt, "DCA_Action"] = 1.0
                i += period


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
