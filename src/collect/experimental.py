import numpy
import pandas as pd
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn.metrics import auc
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

df = pd.read_json('../db/phase5/result.json')
del df['away_team-name']
del df['home_name']
del df['away_name']
del df['home_team-name']
del df['away_date']
del df['away_is-won']
del df['home_date']
del df['away_games-count']
del df['home_home-game']

# print len(df.index)
df = df[df['home_games-count'] > 10]
# df = df[df['year'] == 2010]
del df['home_games-count']
del df['year']
# print len(df.index)
df.fillna(value=0, inplace=True)

features_df = pd.get_dummies(df)

del features_df['home_is-won']

#  monkey mode
# for key in df.keys():
#     if 'year' not in key and 'home_is-won' not in key:
#         del df[key]

# df_null = df.isnull().unstack()
# t = df_null[df_null]
# away_p10-2pts-made-avg
# print df.loc([92])
# print t
X = features_df.as_matrix()

y = df['home_is-won'].as_matrix()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

learning_rates = [1]
train_results = []
test_results = []
for eta in learning_rates:
    model = GradientBoostingClassifier(learning_rate=eta)
    model.fit(x_train, y_train)
    train_pred = model.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    y_pred = model.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

mse = mean_absolute_error(y_train, model.predict(x_train))
print("Training Set Mean Absolute Error: %.4f" % mse)

# Find the error rate on the test set using the best parameters
mse = mean_absolute_error(y_test, model.predict(x_test))
print("Test Set Mean Absolute Error: %.4f" % mse)


line1, = plt.plot(learning_rates, train_results, 'b', label="Train AUC")
line2, = plt.plot(learning_rates, test_results, 'r', label="Test AUC")
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('learning rate')
plt.show()
