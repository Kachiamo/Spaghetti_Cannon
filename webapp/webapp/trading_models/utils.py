import logging

from backtesting.utils import backtest
from .ml_models import train_logistic_regression, train_svc


logging.basicConfig()
log = logging.getLogger(__name__)


ML_MODEL_CHOICES = [
    ("logistic_regression", "logistic regression"),
    ("svc", "support vector classification"),
]

ML_MODELS = {
    "logistic_regression": train_logistic_regression,
    "svc": train_svc,
}

def train_trading_model(trading_model):
    # probably not the best name, but returns a strategy with df, signals, actions, and plotting
    strategy = backtest(trading_model.strategy, trading_model.symbol, trading_model.period)

    # get X_train and y_train
    # Get the length for training data size
    train_length = round(len(strategy.df.keys())*trading_model.training_percent)

    # Clean the data for training
    df = strategy.df.dropna()

    # Get the training dataframe
    train = df[:train_length]

    # Get the name of the action column
    y_column = f"{strategy.strategy}_Action"
    y_train = train[y_column]
    X_train = train.drop(columns=[y_column])

    # Get the model class
    model_class = ML_MODELS.get(trading_model.ml_model)

    # Instantiate the model with the X and y train data
    model_instance = model_class(X_train, y_train)

    # Save the model and its score
    log.critical(f"{trading_model.symbol} {trading_model.strategy} Training Data Score: {model_instance.score(X_train, y_train)}")
