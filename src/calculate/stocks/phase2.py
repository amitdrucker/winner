# add local 2 hours min / max per each batch

import json

from stocks.utils import time_to_date_obj, BATCH_TIME_FRAME_SECONDS, MIN_GAIN


def check_rise(value, batch, start_index):
    for i in range(start_index, len(batch)):
        if batch[i]['Value'] - MIN_GAIN > value:
            return True
    return False


def populate_future_rise_in_batch(batch):
    for i in range(0, len(batch) - 1):
        row = batch[i]
        row['Will_Rise'] = check_rise(row['Value'], batch, i + 1)
    row = batch[len(batch) - 1]
    row['Will_Rise'] = False


def enrich_rows_min_max(json_data):
    row = json_data[0]
    entry_time = time_to_date_obj(row['Time'])
    batch = []
    for row in json_data:
        current_time = time_to_date_obj(row['Time'])
        if (current_time - entry_time).seconds >= BATCH_TIME_FRAME_SECONDS:
            populate_future_rise_in_batch(batch)
            entry_time = current_time
            batch = []
        batch.append(row)
    populate_future_rise_in_batch(batch)


def run(year):
    data = json.loads(open('stocks/data/phase2/2018.json', 'r').read())
    enrich_rows_min_max(data)
    open('stocks/data/phase3/%s.json' % year, 'w').write(json.dumps(data))


for year in range(2018, 2019):
    run(str(year))
