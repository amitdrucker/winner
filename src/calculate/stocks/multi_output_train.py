import joblib
import tensorflow
from numpy.random import seed
from sklearn import ensemble
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression, RidgeCV, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from stocks.stocks_prepareDF import prepareDf

seed(1)
tensorflow.compat.v1.set_random_seed(2)


def report(i, y, z):
    print(i)


def train():
    x_train, x_test, y_train, y_test = prepareDf()
    ESTIMATORS = {
        "Extra trees": ExtraTreesRegressor(n_estimators=10,
                                           max_features=32,  # Out of 20000
                                           random_state=0),
        "K-nn": KNeighborsRegressor(),  # Accept default parameters
        "Linear regression": LinearRegression(),
        "Ridge": RidgeCV(),
        "Lasso": Lasso(),
        "ElasticNet": ElasticNet(random_state=0),
        "RandomForestRegressor": RandomForestRegressor(max_depth=4, random_state=2),
        "Decision Tree Regressor": DecisionTreeRegressor(max_depth=5),
        "MultiO/P GBR": MultiOutputRegressor(GradientBoostingRegressor(n_estimators=5)),
        "MultiO/P AdaB": MultiOutputRegressor(AdaBoostRegressor(n_estimators=5))
    }

    y_mse = dict()

    for name, estimator in ESTIMATORS.items():
        estimator.fit(x_train, y_train)  # fit() with instantiated object
        print("Training Set Mean Absolute Error for %s: %.4f" % (name, y_mse[name]))
        y_mse[name] = mean_absolute_error(y_train, estimator.predict(x_train))
        print("Test Set Mean Absolute Error for %s: %.4f" % (name, y_mse[name]))
        y_mse[name] = mean_absolute_error(y_test, estimator.predict(x_test))
