import logging

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import svm
from strategies.utils import STRATEGIES

logging.basicConfig()
log = logging.getLogger(__name__)


def train_logistic_regression(X_train, y_train):
    ml_model = LogisticRegression(solver="lbfgs", random_state=1)
    ml_model.fit(X_train, y_train)
    return ml_model


def train_svc(X_train, y_train):
    ml_model = svm.SVC()
    ml_model.fit(X_train, y_train)
    return ml_model
