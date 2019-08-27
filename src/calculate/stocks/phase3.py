# add prev values and volume x records backs

import json

from stocks.utils import EVENTS_BACK


def add_prev_x(json_data, x):
    for i in range(EVENTS_BACK, len(json_data)):
        row = json_data[i]
        prev_row = json_data[i - x]
        row['prev_%s_value' % str(x)] = prev_row['Value']
        # row['prev_%s_volume' % str(x)] = prev_row['Volume']


def run(year):
    data = json.loads(open('data/phase3/2018.json', 'r').read())
    for x in range(1, EVENTS_BACK + 1):
        add_prev_x(data, x)
    data = data[EVENTS_BACK:]
    open('data/phase4/%s.json' % year, 'w').write(json.dumps(data))


for year in range(2018, 2019):
    run(str(year))
