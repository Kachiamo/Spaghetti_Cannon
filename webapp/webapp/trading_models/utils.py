import logging

import pandas as pd
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

    # Get the model class
    model_class = ML_MODELS.get(trading_model.ml_model)

    # Instantiate the model and get the parameters
    model, parameters = model_class()
    log.critical(f"all paramters: {parameters}")

    # Grid search the model
    gs = GridSearchCV(model, parameters)
    gs.fit(X_train, y_train)

    # Get grid search results
    results = pd.DataFrame(gs.cv_results_)
    # order by rank_test_score
    sorted = results.sort_values('rank_test_score')
    params = sorted.loc[sorted.index[0]]["params"]
    log.critical(f"optimal paramters: {params}")

    # Save the optimal parameters
    trading_model.optimal_parameters = params
    trading_model.save()
