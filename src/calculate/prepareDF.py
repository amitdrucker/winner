import numpy as np
import pandas as pd
import tensorflow as tf


def remove_all_is_won(df, preDiff):
    for j in range(-12, 13):
        if j != preDiff:
            del df['home_is-won_' + str(j)]
        del df['away_is-won_' + str(j)]


def prepareDf(testYear, preDiff=0):
    df = pd.read_json('../../db/phase5/result.json')
    del df['home_score-diff-avg']
    del df['away_score-diff-avg']
    del df['home_team-name']
    del df['away_team-name']
    del df['home_name']
    del df['away_name']
    del df['away_date']
    del df['home_date']
    del df['away_games-count']
    del df['home_home-game']
    del df['away_home-game']
    remove_all_is_won(df, preDiff)
    df = df[df['home_round'] > 5]
    x_test_rounds = np.array(df[df['year'] == testYear]['home_round'])
    del df['home_round']
    del df['away_round']
    del df['home_games-count']
    df.fillna(value=0, inplace=True)
    dropColumns = ['home_is-won_' + str(preDiff), 'year']
    # dropColumns = ['year']
    x_train = np.array(df[df['year'] != testYear].drop(columns=dropColumns).values, dtype=np.float64)
    x_test = np.array(df[df['year'] == testYear].drop(columns=dropColumns).values, dtype=np.float64)
    y_train = np.array(df[df['year'] != testYear]['home_is-won_' + str(preDiff)].values, dtype=np.float64)
    y_test = np.array(df[df['year'] == testYear]['home_is-won_' + str(preDiff)].values, dtype=np.float64)
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)
    return x_train, x_test, y_train, y_test, x_test_rounds
