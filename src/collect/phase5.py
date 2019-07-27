import json


def normalizeDate(date):
    date = date.strip()
    if len(date) == 10:
        return date + '00:00'
    return date


def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def run(year, result):
    print 'working on year %s' % str(year)
    print '-------------------'
    phase1Data = json.loads(open('../../db/phase1/%s.json' % year, 'r').read())
    phase4Data = json.loads(open('../../db/phase4/%s.json' % year, 'r').read())
    for p2Entry in phase1Data:
        home = p2Entry['home']
        away = p2Entry['away']
        date = normalizeDate(p2Entry['date'])
        homeData = phase4Data[home][date]
        for key, value in homeData.items():
            homeData['home_' + key] = value
            del homeData[key]
        homeData['home_name'] = home
        awayData = phase4Data[away][date]
        for key, value in awayData.items():
            awayData['away_' + key] = value
            del awayData[key]
        awayData['away_name'] = away
        dataObj = merge_two_dicts(homeData, awayData)
        dataObj['year'] = year
        result.append(dataObj)


result = []
for i in range(2003, 2020):
    run(str(i), result)
open('../../db/phase5/result.json', 'w').write(json.dumps(result))
