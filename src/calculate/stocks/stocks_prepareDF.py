import json

import numpy as np
import pandas as pd
from tensorflow.contrib import keras

from stocks.utils import print_nans, TEST_MONTHS, TRAIN_MONTHS


def prepare_df_for_train():
    as_json = json.loads(open('data/phase3/result.json', 'r').read())
    df = pd.DataFrame(as_json)
    print_nans(df)
    df = df.dropna()
    print_nans(df)
    # train_data_max = datetime.strptime('%s-%s-01' % (str(year), TRAIN_DATA_MONTHS), '%Y-%m-%d')
    drop_columns_x = ['Will_Raise', 'Date', 'Month', 'Batch_ID']
    # drop_columns_x = ['Date', 'Month']
    keep_column_y = 'Will_Raise'
    # x = np.array(df.drop(columns=drop_columns_x).values, dtype=np.float64)
    # y = np.array(df[keep_column_y].values, dtype=np.float64)
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    df_train = df
    df_test = df
    for month in TEST_MONTHS:
        df_train = df_train[df_train['Month'] != month]
    for month in TRAIN_MONTHS:
        df_test = df_test[df_test['Month'] != month]
    x_train = np.array(df_train.drop(columns=drop_columns_x).values, dtype=np.float64)
    x_test = np.array(df_test.drop(columns=drop_columns_x).values, dtype=np.float64)
    y_train = np.array(df_train[keep_column_y].values, dtype=np.float64)
    y_test = np.array(df_test[keep_column_y].values, dtype=np.float64)
    x_train = keras.utils.normalize(x_train, axis=1)
    x_test = keras.utils.normalize(x_test, axis=1)
    return x_train, x_test, y_train, y_test


def prepare_df_for_test():
    as_json = json.loads(open('data/phase3/result.json', 'r').read())
    df = pd.DataFrame(as_json)
    print_nans(df)
    df = df.dropna()
    print_nans(df)
    for month in TRAIN_MONTHS:
        df = df[df['Month'] != month]
    return df
