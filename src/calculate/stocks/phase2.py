# add local 2 hours min / max per each batch

import json

from stocks.utils import time_to_date_obj, BATCH_TIME_FRAME_SECONDS, MIN_GAIN, convert_arr_to_pd_stock


def check_rise(value, batch, start_index):
    for i in range(start_index, len(batch)):
        if batch[i]['Value'] - MIN_GAIN > value:
            return True
    return False


def get_mid(batch):
    mid_index = round((len(batch) - 1) / 2)
    mid = batch[mid_index]
    rise = 0
    fall = 0
    values = [batch[0]['Value']]
    for i in range(1, mid_index):
        row = batch[i]
        prev_row = batch[i - 1]
        value = row['Value']
        if value >= prev_row['Value']:
            rise += 1
        else:
            fall += 1
        values.append(value)

    stock = convert_arr_to_pd_stock(batch[:mid_index + 1])
    # from https://pypi.org/project/stockstats/
    result = {'Will_Rise': check_rise(mid['Value'], batch, mid_index + 1), 'Prev_Rise_Count': rise,
              'Prev_Fall_Count': fall, 'Date': mid['Date'], 'cr': stock['cr'].iloc[mid_index],
              'cr-ma1': stock['cr-ma1'].iloc[mid_index], 'cr-ma2': stock['cr-ma2'].iloc[mid_index],
              'cr-ma3': stock['cr-ma3'].iloc[mid_index], 'kdjk': stock['kdjk'].iloc[mid_index],
              'kdjd': stock['kdjd'].iloc[mid_index], 'kdjj': stock['kdjj'].iloc[mid_index],
              'macd': stock['macd'].iloc[mid_index], 'macds': stock['macds'].iloc[mid_index],
              'macdh': stock['macdh'].iloc[mid_index], 'boll': stock['boll'].iloc[mid_index],
              'boll_ub': stock['boll_ub'].iloc[mid_index], 'boll_lb': stock['boll_lb'].iloc[mid_index],
              'rsi_6': stock['rsi_6'].iloc[mid_index], 'rsi_12': stock['rsi_12'].iloc[mid_index],
              'wr_10': stock['wr_10'].iloc[mid_index], 'wr_6': stock['wr_6'].iloc[mid_index],
              'cci': stock['cci'].iloc[mid_index], 'cci_20': stock['cci_20'].iloc[mid_index],
              'tr': stock['tr'].iloc[mid_index], 'atr': stock['atr'].iloc[mid_index],
              'dma': stock['dma'].iloc[mid_index], 'pdi': stock['pdi'].iloc[mid_index],
              'mdi': stock['mdi'].iloc[mid_index], 'dx': stock['dx'].iloc[mid_index],
              'adx': stock['adx'].iloc[mid_index], 'adxr': stock['adxr'].iloc[mid_index],
              'trix': stock['trix'].iloc[mid_index], 'trix_9_sma': stock['trix_9_sma'].iloc[mid_index],
              'tema': stock['tema'].iloc[mid_index], 'vr': stock['vr'].iloc[mid_index],
              'vr_6_sma': stock['vr_6_sma'].iloc[mid_index]}
    return result


def transform_to_mid(json_data):
    result = []
    row = json_data[0]
    entry_time = time_to_date_obj(row['Time'])
    batch = []
    counter = 0
    for row in json_data:
        print(str(len(json_data) - counter))
        counter += 1
        current_time = time_to_date_obj(row['Time'])
        if (current_time - entry_time).seconds >= BATCH_TIME_FRAME_SECONDS:
            if len(batch) > 40:
                result.append(get_mid(batch))
            entry_time = current_time
            batch = []
        batch.append(row)
    if len(batch) > 40:
        result.append(get_mid(batch))
    return result


def run():
    data = json.loads(open('data/phase2/result.json', 'r').read())
    data = transform_to_mid(data)
    open('data/phase3/result.json', 'w').write(json.dumps(data))


run()
