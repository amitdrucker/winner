import json
from datetime import datetime

import pandas as pd

# 1min: Date,Time,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose
# tick: Date,Time,Open,High,Low,Close,Volume
# original file collected from http://api.kibot.com/?action=history&symbol=IVE&interval=tickbidask&bp=1&user=guest
import csv


def get_object_by_index(data, index):
    return {
        'Date': data['Date'][index],
        'Time': data['Time'][index],
        'High': data['High'][index],
        'Low': data['Low'][index],
        'Open': data['Open'][index],
        'Volume': data['Volume'][index]
    }


def merge_rows(df):
    json_df = json.loads(df.to_json())
    new_json = []
    entry = None
    keys = json_df['Time'].keys()
    for index in json_df['Time'].keys():
        print(str(len(keys) - int(index)))
        if not entry:
            entry = get_object_by_index(json_df, index)
            continue
        current = get_object_by_index(json_df, index)
        current_time = datetime.strptime(current['Time'], '%H:%M:%S')
        entry_time = datetime.strptime(entry['Time'], '%H:%M:%S')
        if (current_time - entry_time).seconds < 60:
            entry['Low'] = min(entry['Low'], current['Low'])
            entry['High'] = max(entry['High'], current['High'])
            entry['Volume'] = entry['Volume'] + current['Volume']
        else:
            new_json.append(entry)
            entry = current
    return new_json


# f = open('stocks/IVE_tickbidask_2018.csv', 'r')
df = pd.read_csv('stocks/IVE_tickbidask_2018.csv')
df = df['09:30:00' < df['Time']]
df = df[df['Time'] < '16:00:00']
open('stocks/temp.json', 'w').write(json.dumps(merge_rows(df)))
df = pd.read_json('stocks/temp.json')
df.to_cs('stocks/test.csv')
exit(0)
entries_back = 20
for i in range(1, entries_back):
    df['%d-back-max-price-diff-pct' % i] = 0
    df['%d-back-volume-diff' % i] = 0
for i in range(entries_back, len(df)):
    for j in range(1, entries_back + 1):
        df.loc[i, '%d-back-max-to-open-ratio' % j] = \
            df.loc[i - j, 'High'] / df.loc[i, 'Open']
        df['%d-back-volume-diff' % i] = df.loc[i - j, 'Volume'] / df.loc[i, 'Volume']

    df.loc[i, '%d-back-max-price-diff-pct' % i] = df.loc[i - 1, 'C'] * df.loc[i, 'A'] + df.loc[i, 'B']

# reader = csv.DictReader(f, fieldnames=('Index', 'Date', 'Time', 'Open', 'Low', 'High', 'Volume'))
# db = remove_open_day_traffic([row for row in reader][2:])

print('')
