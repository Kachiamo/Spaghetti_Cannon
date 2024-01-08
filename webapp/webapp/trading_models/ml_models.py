import logging

from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from strategies.utils import STRATEGIES

logging.basicConfig()
log = logging.getLogger(__name__)


def get_logistic_regression():
    parameters = {
        "C": [
            1,
            5,
            15,
            20,
        ],
        "solver": [
            "lbfgs",
            "liblinear",
            "newton-cg",
            "newton-cholesky",
        ],
        "max_iter": [
            50,
            100,
            150,
        ]
    }
    return LogisticRegression(), parameters


def get_random_forest_classifier():
    parameters = {
        "n_estimators": [
            50,
            100,
            150,
            200,
        ],
        "criterion": [
            "gini",
            "entropy",
            "log_loss",
        ],
        "max_features": [
            "sqrt",
            "log2",
        ],
        "class_weight": [
            "balanced",
            "balanced_subsample",
        ]
    }
    return RandomForestClassifier(), parameters


def get_svc():
    parameters = {
        "kernel": [
            "linear",
            "rbf",
            "sigmoid",
        ],
        "C": [
            1,
            5,
            15,
            20,
        ],
        "degree": [
            1,
            5,
            10,
            20,
        ]
    }
    return svm.SVC(), parameters
