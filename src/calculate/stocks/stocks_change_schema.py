import pandas as pd

# 1min: Date,Time,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose
# tick: Date,Time,Open,High,Low,Close,Volume
# original file collected from http://api.kibot.com/?action=history&symbol=IVE&interval=tickbidask&bp=1&user=guest
import csv


def mergeRows(df):
    for i in range(len(df) - 2, -1, -1):
        if df.iloc[i]['Time'] == df.iloc[i - 1]['Time']:
            df.iloc[i - 1]['Low'] = min(df.iloc[i - 1]['Low'], df.iloc[i]['Low'])
            df.iloc[i - 1]['High'] = max(df.iloc[i - 1]['High'], df.iloc[i]['High'])
            df.iloc[i - 1]['Volume'] = df.iloc[i]['Volume'] + df.iloc[i - 1]['Volume']
            df.drop(i)
    return df


# f = open('stocks/IVE_tickbidask_2018.csv', 'r')
df = pd.read_csv('stocks/IVE_tickbidask_2018.csv')
df = df['09:30:00' < df['Time']]
df = df[df['Time'] < '16:00:00']
df = mergeRows(df)
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
