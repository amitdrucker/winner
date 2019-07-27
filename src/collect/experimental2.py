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
del df['year']
del df['away_date']
del df['away_is-won']
del df['home_date']
del df['away_games-count']
del df['home_home-game']

# print len(df.index)
df = df[df['home_games-count'] > 5]
del df['home_games-count']
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

import matplotlib.pyplot as plt
import seaborn as sns

# Plot formatting
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 18
plt.figure(figsize=(8, 8))

# Plot each point as the label
for x1, x2, label in zip(X[:, 0], X[:, 1], y):
    plt.text(x1, x2, str(label), fontsize=40, color='g',
             ha='center', va='center')

# Plot formatting
plt.grid(None)
plt.xlim((0, 3.5))
plt.ylim((0, 3.5))
plt.xlabel('x1', size=20)
plt.ylabel('x2', size=20)
plt.title('Data', size=24)
plt.show()
