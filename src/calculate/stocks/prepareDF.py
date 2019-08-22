from datetime import datetime

import numpy as np
import pandas as pd
import tensorflow as tf

from stocks.utils import TRAIN_DATA_MONTHS

year = 2018

df = pd.read_json('data/phase4/2018.json')
train_data_max = datetime.strptime('%s-%s-01' % (str(year), TRAIN_DATA_MONTHS), '%Y-%m-%d')
drop_columns = ['Will_Rise', 'Date', 'Time']
x_train = np.array(df[df['Date'] < train_data_max].drop(columns=drop_columns).values, dtype=np.float64)
x_test = np.array(df[df['Date'] >= train_data_max].drop(columns=drop_columns).values, dtype=np.float64)
y_train = np.array(df[df['Date'] < train_data_max][drop_columns[0]].values, dtype=np.float64)
y_test = np.array(df[df['Date'] >= train_data_max][drop_columns[0]].values, dtype=np.float64)
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
