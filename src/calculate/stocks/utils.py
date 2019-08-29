from datetime import datetime

# 2 hours
import numpy as np
import pandas as pd
from stockstats import StockDataFrame

BATCH_TIME_FRAME_SECONDS = 60 * 60 * 2
TEST_MONTHS = ['03', '06', '09', '12']
TRAIN_MONTHS = ['01', '02', '04', '05', '07', '08', '10', '11']
MIN_GAIN = 0.1
EVENTS_BACK = 3
TRAIN_DATA_MONTHS = 10


def print_nans(df):
    print('NaNs:')
    for col in df.columns:
        if col != 'Date' and col != 'Month':
            indexes = df[col].index[df[col].apply(np.isnan)]
            if len(indexes) > 0:
                print(col + ', ' + str(len(indexes)))


def time_to_date_obj(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')


def date_to_date_obj(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')


def mean(a, b):
    return (a + b) / 2


def to_stocks_array(arr):
    result = []
    for row in arr:
        result.append([
            row['Value'],
            row['Value'],
            row['Value'],
            row['Value'],
            row['Volume'],
            row['Volume']
        ])
    return result


def convert_arr_to_pd_stock(arr):
    df = pd.DataFrame(columns=['open', 'close', 'high', 'low', 'volume', 'amount'], data=to_stocks_array(arr))
    stock = StockDataFrame.retype(df)
    return stock
