import logging

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import svm
from strategies.utils import STRATEGIES
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig()
log = logging.getLogger(__name__)


def train_logistic_regression(X_train, y_train):
    ml_model = LogisticRegression(solver="lbfgs", random_state=1)
    ml_model.fit(X_train, y_train)
    return ml_model

def train_random_forest_classifier(X_train, y_train):
    ml_model = RandomForestClassifier(n_estimators=100, random_state=1)
    ml_model.fit(X_train, y_train)
    return ml_model

def train_svc(X_train, y_train):
    ml_model = svm.SVC()
    ml_model.fit(X_train, y_train)
    return ml_model
