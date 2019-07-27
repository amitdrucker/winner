import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, ShuffleSplit

rf = RandomForestClassifier(max_features=10, n_estimators=10, oob_score=True)
param_grid = {'min_samples_leaf': range(1, 5, 2),
              'max_features': range(1, 6, 2),
              'n_estimators': range(50, 250, 50)}

inner_cv = ShuffleSplit(n_splits=3, train_size=0.5)
gs = GridSearchCV(estimator=rf, param_grid=param_grid, cv=inner_cv,
                  verbose=100)

rng = np.random.RandomState(0)
train_data = rng.rand(416, 70000)
train_labels = rng.randint(0, 2, 416)

gs.fit(train_data, train_labels)
