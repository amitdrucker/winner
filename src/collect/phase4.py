import json
from datetime import datetime

import copy
from statistics import stdev


def calcGradientAvg(field, prevDO, prevPrevDO):
    if not prevDO:
        return 0
    if not prevPrevDO:
        return prevDO[field]
    return '%.3f' % float((float(prevPrevDO[field + '-avg']) +
                           float(prevDO[field])) / 2)


def calcStdev(field, index, teamArr):
    if index < 2:
        return 0
    arr = []
    for j in range(0, index):
        if field[0] == 'p' and field not in teamArr[j]:
            arr.append(0)
        else:
            arr.append(teamArr[j][field])
    return '%.3f' % (stdev(tuple(arr)))


def findIndexByDate(date, teamArr):
    date = datetime.strptime(date, '%d/%m/%Y%H:%M')
    for j in range(0, len(teamArr)):
        if datetime.strptime(teamArr[j]['date'], '%d/%m/%Y%H:%M') >= date:
            return j
    return j


def getGamesCount(teamArr, date):
    return findIndexByDate(date, teamArr)


def run(year):
    print 'working on %s' % str(year)
    print '---------------'
    data = json.loads(open('../../db/phase3/%s.json' % year, 'r').read())
    for teamName, teamArr in data.items():
        print 'team %s' % teamName
        data[teamName] = {'array': teamArr, 'dict': {}}
        prevDO = None
        prevPrevDO = None
        for j in range(0, len(teamArr)):
            originalDataObj = teamArr[j]
            dataObj = copy.deepcopy(originalDataObj)
            for field in dataObj.keys():
                if field not in excludedFields:
                    dataObj[field + '-avg'] = calcGradientAvg(field, prevDO, prevPrevDO)
                    originalDataObj[field + '-avg'] = dataObj[field + '-avg']
                    # if field not in excludedStdevFields:
                    #     dataObj[field + '-stdev'] = calcStdev(field, j, teamArr)
                    if field not in excludedRemoveFields:
                        del dataObj[field]
            dataObj['games-count'] = getGamesCount(teamArr, dataObj['date'])
            data[teamName]['dict'][dataObj['date']] = dataObj
            prevPrevDO = prevDO
            prevDO = originalDataObj
        data[teamName] = data[teamName]['dict']
    open('../../db/phase4/%s.json' % year, 'w').write(json.dumps(data))


excludedFields = ['home-game', 'team-name', 'date', 'round']
excludedRemoveFields = ['is-won', 'win-by-diff']
excludedStdevFields = ['is-won', 'win-by-diff']
for i in range(2003, 2020):
    run(str(i))
