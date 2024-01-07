import logging

from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import DateOffset

from backtesting.utils import backtest
from .ml_models import train_logistic_regression, train_svc, train_random_forest_classifier


logging.basicConfig()
log = logging.getLogger(__name__)


ML_MODEL_CHOICES = [
    ("logistic_regression", "logistic regression"),
    ("svc", "support vector classification"),
    ("rfc", "random forest classifier"),
]

ML_MODELS = {
    "logistic_regression": train_logistic_regression,
    "svc": train_svc,
    "rfc": train_random_forest_classifier,
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

    # Instantiate the model with the X and y train data
    model_instance = model_class(X_train, y_train)

    # Save the model and its score
    log.critical(f"{trading_model.symbol} {trading_model.strategy} Training Data Score: {model_instance.score(X_train, y_train)}")
