import pandas as pd
import sklearn
from keras import Input
from keras import Model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import BatchNormalization, Dropout, Dense, K
from keras.losses import mean_squared_error, mean_squared_logarithmic_error, mean_absolute_error, binary_crossentropy
from sklearn import ensemble
from sklearn.model_selection import train_test_split

df = pd.read_json('../../db/phase5/result.json')
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

for col in df.columns:
    if '_p' in col or 'israeli' in col or 'foreign' in col:
        del df[col]

print df.columns

df = df[df['home_games-count'] > 5]
del df['home_games-count']
df.fillna(value=0, inplace=True)
features_df = pd.get_dummies(df)
del features_df['home_is-won']
print len(features_df.index)


def get_model(input_dim, output_dim, base=1000, multiplier=0.25, p=0.2):
    inputs = Input(shape=(input_dim,))
    l = BatchNormalization()(inputs)
    l = Dropout(p)(l)
    n = base
    l = Dense(n, activation='relu')(l)
    l = BatchNormalization()(l)
    l = Dropout(p)(l)
    n = int(n * multiplier)
    l = Dense(n, activation='relu')(l)
    l = BatchNormalization()(l)
    l = Dropout(p)(l)
    n = int(n * multiplier)
    l = Dense(n, activation='relu')(l)
    outputs = Dense(output_dim, activation='softmax')(l)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='Nadam', loss=binary_crossentropy)
    return model


# model = get_model(276, 1, 100, 0.9, 0.7)
model = get_model(4, 1, 100, 0.9, 0.7)

X = features_df.as_matrix()
y = df['home_is-won'].as_matrix()

train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=0)

history = model.fit(train_x, train_y, validation_data=(test_x, test_y),
                    epochs=200, batch_size=5,
                    callbacks=[EarlyStopping(patience=25),
                               ModelCheckpoint('mean_absolute_error.hdf5', save_best_only=True)])
print(
    'Training Loss : {}\nValidation Loss : {}'.format(model.evaluate(train_x, train_y), model.evaluate(test_x, test_y)))
exit(0)

# Parameters we want to try
model = ensemble.GradientBoostingRegressor(
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=6,
    min_samples_leaf=5,
    max_features=0.3,
    loss='huber',
    random_state=0
)

# model.fit(X_train, y_train)
#
# # Find the error rate on the training set using the best parameters
# mse = mean_absolute_error(y_train, model.predict(X_train))
# print("Training Set Mean Absolute Error: %.4f" % mse)
#
# # Find the error rate on the test set using the best parameters
# mse = mean_absolute_error(y_test, model.predict(X_test))
# print("Test Set Mean Absolute Error: %.4f" % mse)
#
# # Save the trained model to a file so we can use it in other programs
# joblib.dump(model, '../output/trained_basketball_win_predictor.pkl')
