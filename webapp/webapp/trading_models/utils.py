import logging

import pandas as pd
from pathlib import Path
import pickle
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from backtesting.utils import backtest
from .ml_models import (
    get_logistic_regression,
    get_svc,
    get_random_forest_classifier
)

logging.basicConfig()
log = logging.getLogger(__name__)


ML_MODEL_CHOICES = [
    ("logistic_regression", "logistic regression"),
    ("svc", "support vector classification"),
    ("rfc", "random forest classifier"),
]

ML_MODELS = {
    "logistic_regression": get_logistic_regression,
    "svc": get_svc,
    "rfc": get_random_forest_classifier,
}


def backtest_strategy(trading_model):
    try:
        strategy = backtest(trading_model.strategy, trading_model.symbol, trading_model.period)
        strategy.add_position_and_returns()
        trading_model.strategy_returns = strategy.df.iloc[-1]["Strategy_Cumulative_Returns"]
        trading_model.symbol_returns = strategy.df.iloc[-1]["Stock_Cumulative_Returns"]
        trading_model.save()
    except Exception:
        log.exception("Shrug")
        pass


def backtest_model(trading_model):
    pass


def train_trading_model(trading_model):
    # probably not the best name, but returns a strategy with df, signals, actions, and plotting
    strategy = backtest(trading_model.strategy, trading_model.symbol, trading_model.period)

    # Clean the data for training
    df = strategy.df.dropna()

    # Get the name of the action column
    y_column_name = f"{strategy.strategy}_Action"
    y = df[y_column_name]

    # Drop columns that are not features
    df = df[strategy.features]

    # get X_train and y_train
    # Get the length for training data size
    train_start = df.index[0]
    time_delta = relativedelta(df.index[-1], train_start)
    total_months = time_delta.months + time_delta.years*12
    train_months = round(total_months*trading_model.training_percent)
    train_end_date = train_start + DateOffset(months=train_months)

    # Get the training dataframe
    X_train = df[:train_end_date]
    y_train = y[:train_end_date]
    X_test = df[train_end_date:]
    y_test = y[train_end_date:]

    # Get the model class
    model_class = ML_MODELS.get(trading_model.ml_model)

    # Instantiate the model and get the parameters
    model, parameters = model_class()
    log.critical(f"all paramters: {parameters}")

    # Grid search the model
    gs = GridSearchCV(model, parameters)
    gs.fit(X_train, y_train)
    best_model = gs.best_estimator_
    log.critical(f'best_model {best_model}')

    # Write the model to disk
    path = Path(f"trained_models/{trading_model.uuid}.pickle")
    pickled_model = pickle.dumps(best_model)
    with open(path, "wb") as binary_file:
        # Write bytes to file
        binary_file.write(pickled_model)

    # Compute the model returns
    strategy.df[y_column_name] = best_model.predict(strategy.df[strategy.features].fillna(0))
    strategy.add_position_and_returns()
    trading_model.model_returns = strategy.df.iloc[-1]["Strategy_Cumulative_Returns"]

    # Get model predictions
    predictions = best_model.predict(X_test)
    precision = precision_score(y_test, predictions, average=None)
    recall = recall_score(y_test, predictions, average=None)
    log.critical(f"precision {precision} recall {recall}")

    report = classification_report(y_test, predictions, zero_division=1)
    log.critical(report)

    try:
        precision_sell, precision_hold, precision_buy = precision
        recall_sell, recall_hold, recall_buy = recall
    except Exception:
        # Some strategies have no hold...
        # only buy/sell
        precision_hold = 0
        recall_hold = 0
        precision_sell, precision_buy = precision
        recall_sell, recall_buy = recall

    # Save the optimal parameters, accuracy, recall, and precision
    trading_model.optimal_parameters = gs.best_params_
    trading_model.accuracy = accuracy_score(y_test, predictions)
    trading_model.precision_buy = precision_buy
    trading_model.precision_sell = precision_sell
    trading_model.precision_hold = precision_hold
    trading_model.recall_buy = recall_buy
    trading_model.recall_sell = recall_sell
    trading_model.recall_hold = recall_hold
    trading_model.save()
