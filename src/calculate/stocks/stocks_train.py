import joblib
import tensorflow
from numpy.random import seed
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error

from stocks.stocks_prepareDF import prepareDf

seed(1)
tensorflow.compat.v1.set_random_seed(2)


def report(i, y, z):
    print(i)


def train():
    x_train, x_test, y_train, y_test = prepareDf()
    model = ensemble.GradientBoostingRegressor(
        n_estimators=20000,
        learning_rate=0.1,
        max_depth=6,
        min_samples_leaf=9,
        max_features=0.1,
        loss='huber',
        random_state=0
    )
    model.fit(x_train, y_train, monitor=report)

    # Save the trained model to a file so we can use it in other programs
    joblib.dump(model, 'trained.pkl')

    # Find the error rate on the training set
    mse = mean_absolute_error(y_train, model.predict(x_train))
    print("Training Set Mean Absolute Error: %.4f" % mse)

    # Find the error rate on the test set
    mse = mean_absolute_error(y_test, model.predict(x_test))
    print("Test Set Mean Absolute Error: %.4f" % mse)
