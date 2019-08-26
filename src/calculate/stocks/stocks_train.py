import joblib
from numpy.random import seed
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error

from stocks.stocks_prepareDF import prepareDf

seed(1)
from tensorflow import set_random_seed

set_random_seed(2)


def report(i, y, z):
    print(i)


def train(test_year):
    x_train, x_test, y_train, y_test = prepareDf(test_year)
    model = ensemble.GradientBoostingRegressor(
        n_estimators=500,
        learning_rate=0.1,
        max_depth=6,
        min_samples_leaf=6,
        max_features=0.2,
        loss='huber',
        random_state=0
    )
    model.fit(x_train, y_train, monitor=report)

    # Save the trained model to a file so we can use it in other programs
    joblib.dump(model, 'trained_house_classifier_model.pkl')

    # Find the error rate on the training set
    mse = mean_absolute_error(y_train, model.predict(x_train))
    print("Training Set Mean Absolute Error: %.4f" % mse)

    # Find the error rate on the test set
    mse = mean_absolute_error(y_test, model.predict(x_test))
    print("Test Set Mean Absolute Error: %.4f" % mse)
