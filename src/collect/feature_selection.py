import pandas as pd
from sklearn.externals import joblib

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
del df['away_home-game']
del df['home_games-count']
del df['home_is-won']

# These are the feature labels from our data set
feature_labels = list(df.columns.values)

# Load the trained model created with train_model.py
model = joblib.load('../output/trained_basketball_win_predictor.pkl')

# Create a numpy array based on the model's feature importances
importance = model.feature_importances_

# Sort the feature labels based on the feature importance rankings from the model
feature_indexes_by_importance = importance.argsort()

# Print each feature label, from most important to least important (reverse order)
for index in feature_indexes_by_importance:
    print("{} - {:.2f}%".format(feature_labels[index], (importance[index] * 100.0)))
