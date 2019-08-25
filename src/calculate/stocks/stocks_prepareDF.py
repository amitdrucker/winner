from datetime import datetime

import numpy as np
import pandas as pd
import tensorflow as tf

from stocks.utils import TRAIN_DATA_MONTHS


def prepareDf(year):
    df = pd.read_json('data/phase4/2018.json')
    train_data_max = datetime.strptime('%s-%s-01' % (str(year), TRAIN_DATA_MONTHS), '%Y-%m-%d')
    drop_columns_x = ['Will_Rise', 'Date', 'Time']
    # drop_columns_x = ['Date', 'Time']
    keep_column_y = 'Will_Rise'
    x_train = np.array(df[df['Date'] < train_data_max].drop(columns=drop_columns_x).values, dtype=np.float64)
    x_test = np.array(df[df['Date'] >= train_data_max].drop(columns=drop_columns_x).values, dtype=np.float64)
    y_train = np.array(df[df['Date'] < train_data_max][keep_column_y].values, dtype=np.float64)
    y_test = np.array(df[df['Date'] >= train_data_max][keep_column_y].values, dtype=np.float64)
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)
    return x_train, x_test, y_train, y_test
