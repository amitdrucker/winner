# add local 2 hours min / max per each batch

import json

from stocks.utils import time_to_date_obj, BATCH_TIME_FRAME_SECONDS, MIN_GAIN, convert_arr_to_pd_stock


def check_rise(value, batch, start_index):
    for i in range(start_index, len(batch)):
        if batch[i]['Value'] - MIN_GAIN > value:
            return True
    return False


def enrich_data(batch):
    results = []
    stock = convert_arr_to_pd_stock(batch)
    for i in range(20, len(batch) - 20):
        row = batch[i]
        # from https://pypi.org/project/stockstats/
        result = {'Will_Rise': check_rise(row['Value'], batch, i + 1),
                  'Date': row['Date'], 'Month': row['Date'][0:2], 'cr': stock['cr'].iloc[i],
                  'cr-ma1': stock['cr-ma1'].iloc[i], 'cr-ma2': stock['cr-ma2'].iloc[i],
                  'cr-ma3': stock['cr-ma3'].iloc[i], 'kdjk': stock['kdjk'].iloc[i],
                  'kdjd': stock['kdjd'].iloc[i], 'kdjj': stock['kdjj'].iloc[i],
                  'macd': stock['macd'].iloc[i], 'macds': stock['macds'].iloc[i],
                  'macdh': stock['macdh'].iloc[i], 'boll': stock['boll'].iloc[i],
                  'boll_ub': stock['boll_ub'].iloc[i], 'boll_lb': stock['boll_lb'].iloc[i],
                  'rsi_6': stock['rsi_6'].iloc[i], 'rsi_12': stock['rsi_12'].iloc[i],
                  'wr_10': stock['wr_10'].iloc[i], 'wr_6': stock['wr_6'].iloc[i],
                  'cci': stock['cci'].iloc[i], 'cci_20': stock['cci_20'].iloc[i],
                  'tr': stock['tr'].iloc[i], 'atr': stock['atr'].iloc[i],
                  'dma': stock['dma'].iloc[i], 'pdi': stock['pdi'].iloc[i],
                  'mdi': stock['mdi'].iloc[i], 'dx': stock['dx'].iloc[i],
                  'adx': stock['adx'].iloc[i], 'adxr': stock['adxr'].iloc[i],
                  'trix': stock['trix'].iloc[i], 'trix_9_sma': stock['trix_9_sma'].iloc[i],
                  'tema': stock['tema'].iloc[i], 'vr': stock['vr'].iloc[i],
                  'vr_6_sma': stock['vr_6_sma'].iloc[i]}
        results.append(result)
    return results


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
                result += enrich_data(batch)
            entry_time = current_time
            batch = []
        batch.append(row)
    if len(batch) > 40:
        result += enrich_data(batch)
    return result


def run():
    data = json.loads(open('data/phase2/result.json', 'r').read())
    data = transform_to_mid(data)
    open('data/phase3/result.json', 'w').write(json.dumps(data))


run()
