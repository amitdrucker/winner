import numpy as np
import pandas as pd
import tensorflow as tf


def prepareDf(testYear):
    df = pd.read_json('../db/result.json')
    del df['away_team-name']
    del df['home_name']
    del df['away_name']
    del df['home_team-name']
    del df['away_date']
    del df['away_is-won']
    del df['home_is-won']
    del df['away_win-by-diff']
    del df['home_date']
    del df['away_games-count']
    del df['home_home-game']
    del df['away_home-game']
    del df['home_win-by-diff-avg']
    del df['away_win-by-diff-avg']
    df = df[df['home_round'] > 5]
    x_test_rounds = np.array(df[df['year'] == testYear]['home_round'])
    del df['home_round']
    del df['away_round']
    del df['home_games-count']
    df.fillna(value=0, inplace=True)
    dropColumns = ['home_win-by-diff', 'year']
    # dropColumns = ['year']
    x_train = np.array(df[df['year'] != testYear].drop(columns=dropColumns).values, dtype=np.float64)
    x_test = np.array(df[df['year'] == testYear].drop(columns=dropColumns).values, dtype=np.float64)
    y_train = np.array(df[df['year'] != testYear]['home_win-by-diff'].values, dtype=np.float64)
    y_test = np.array(df[df['year'] == testYear]['home_win-by-diff'].values, dtype=np.float64)
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)
    return x_train, x_test, y_train, y_test, x_test_rounds
