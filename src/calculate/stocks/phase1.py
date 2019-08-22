# create a json file from df

# 1min: Date,Time,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose
# tick: Date,Time,Open,High,Low,Close,Volume
# original file collected from http://api.kibot.com/?action=history&symbol=IVE&interval=tickbidask&bp=1&user=guest


import json

import pandas as pd

from stocks.utils import time_to_date_obj, mean


def get_object_by_index(data, index):
    return {
        'Date': data['Date'][index],
        'Time': data['Time'][index],
        'High': data['High'][index],
        'Low': data['Low'][index],
        'Open': data['Open'][index],
        'Volume': data['Volume'][index]
    }


def create_new_entry(data):
    return {
        'Date': data['Date'],
        'Time': data['Time'],
        'Value': round(mean(data['Low'], data['High']), 2),
        'Volume': data['Volume']
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
            entry_time = time_to_date_obj(entry['Time'])
            continue
        current = get_object_by_index(json_df, index)
        current_time = time_to_date_obj(current['Time'])
        if (current_time - entry_time).seconds < 60:
            entry['Low'] = min(entry['Low'], current['Low'])
            entry['High'] = max(entry['High'], current['High'])
            entry['Volume'] = entry['Volume'] + current['Volume']
        else:
            new_json.append(create_new_entry(entry))
            entry = current
            entry_time = time_to_date_obj(entry['Time'])
    return new_json


def run(year):
    df = pd.read_csv('data/phase1/IVE_tickbidask_%s.csv' % year)
    df = df['09:30:00' < df['Time']]
    df = df[df['Time'] < '16:00:00']
    merged_rows_json = merge_rows(df)
    open('data/phase2/%s.json' % year, 'w').write(json.dumps(merged_rows_json))


for year in range(2018, 2019):
    run(str(year))
