import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.contrib import keras

from stocks.utils import print_nans


def prepareDf():
    as_json = json.loads(open('data/phase3/result.json', 'r').read())
    df = pd.DataFrame(as_json)
    print_nans(df)
    df = df.fillna(0)
    print_nans(df)
    # train_data_max = datetime.strptime('%s-%s-01' % (str(year), TRAIN_DATA_MONTHS), '%Y-%m-%d')
    drop_columns_x = ['Will_Rise', 'Date']
    # drop_columns_x = ['Date']
    keep_column_y = 'Will_Rise'
    x = np.array(df.drop(columns=drop_columns_x).values, dtype=np.float64)
    y = np.array(df[keep_column_y].values, dtype=np.float64)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    x_train = keras.utils.normalize(x_train, axis=1)
    x_test = keras.utils.normalize(x_test, axis=1)
    return x_train, x_test, y_train, y_test
