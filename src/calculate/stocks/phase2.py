# add local 2 hours min / max per each batch

import json

from stocks.utils import mean, to_date_obj

TWO_HOURS_SECONDS = 60 * 60 * 2


def populate_min_max_in_batch(batch, batch_min, batch_max):
    for row in batch:
        current_value = mean(row['High'], row['Low'])
        row['min'] = True if current_value == batch_min else False
        row['max'] = True if current_value == batch_max else False


def enrich_rows_min_max(json_data):
    row = json_data[0]
    batch_min = mean(row['High'], row['Low'])
    batch_max = mean(row['High'], row['Low'])
    entry_time = to_date_obj(row['Time'])
    batch = []
    for row in json_data:
        current_time = to_date_obj(row['Time'])
        current_value = mean(row['High'], row['Low'])
        if (current_time - entry_time).seconds >= TWO_HOURS_SECONDS:
            populate_min_max_in_batch(batch, batch_min, batch_max)
            batch_min = current_value
            batch_max = current_value
            entry_time = current_time
            batch = []
        if current_value < batch_min:
            batch_min = current_value
        if current_value > batch_max:
            batch_max = current_value
        batch.append(row)


def run(year):
    data = json.loads(open('stocks/data/phase2/2018.json', 'r').read())
    enrich_rows_min_max(data)
    open('stocks/data/phase3/%s.json' % year, 'w').write(json.dumps(data))


for year in range(2018, 2019):
    run(str(year))
