import json


def insertRecord(teamName, dataObj, data):
    if teamName not in data:
        data[teamName] = []
    data[teamName].append(dataObj)


def calcScoreDiff(isHome, scoreDiff):
    return scoreDiff * -1 if not isHome else scoreDiff


# 0: below -10
# 1: -8, -9, -10
# 2: -6, -7
# 3: -4, -5
# 4: -1, -2, -3
# 5: 1, 2, 3
# 6: 4, 5
# 7: 6, 7
# 8: 8, 9, 10
# 9: above 10
def calcWinDiff(isHome, scoreDiff):
    if not isHome:
        scoreDiff *= -1
    if scoreDiff < -16:
        return 0
    elif scoreDiff < -8:
        return 1
    elif scoreDiff < -4:
        return 2
    elif scoreDiff < -2:
        return 3
    elif scoreDiff < 0:
        return 4
    elif scoreDiff > 16:
        return 9
    elif scoreDiff > 8:
        return 8
    elif scoreDiff > 4:
        return 7
    elif scoreDiff > 2:
        return 6
    elif scoreDiff > 0:
        return 5


def getAllPlayerKeys(dataObj):
    allPlayerKeys = {}
    for key in dataObj.keys():
        if 'p1-' in key:
            allPlayerKeys[key[3:]] = True
    return allPlayerKeys.keys()


def sortAndReplaceValuesForField(dataObj, field):
    items = []
    for j in range(1, 7):
        key = 'p%s-%s' % (str(j), field)
        items.append(dataObj[key])
    items = sorted(items, reverse=True)
    for j in range(1, 7):
        key = 'p%s-%s' % (str(j), field)
        dataObj[key] = items[j - 1]
    for j in range(7, 14):
        key = 'p%s-%s' % (str(j), field)
        if key in dataObj:
            del dataObj[key]


def sortAllPlayers(dataObj):
    allPlayerKeys = getAllPlayerKeys(dataObj)
    for key in allPlayerKeys:
        sortAndReplaceValuesForField(dataObj, key)


def removeRedundantFields(dataObj):
    del dataObj['awayTotalGames']
    del dataObj['homeTotalGames']
    del dataObj['homeTotalPointsCommitted']
    del dataObj['homeTotalPointsReceived']
    del dataObj['awayTotalPointsCommitted']
    del dataObj['awayTotalPointsReceived']
    del dataObj['homeWonGames']
    del dataObj['awayWonGames']
    del dataObj['opponent-score']
    del dataObj['score-diff']
    del dataObj['q1']
    del dataObj['q2']
    del dataObj['q3']
    del dataObj['q4']
    for key in dataObj.keys():
        if '-dunks' in key:
            del dataObj[key]
    for j in range(1, 7):
        key = 'p%s-open' % j
        if key in dataObj:
            del dataObj[key]


def run(year):
    currentPhase2Data = json.loads(open('../../db/phase2/%s.json' % year, 'r').read())
    data = {}
    for dataObj in currentPhase2Data:
        sortAllPlayers(dataObj)
        dataObj['is-won'] = calcScoreDiff(dataObj['home-game'], dataObj['score-diff']) > 0
        dataObj['win-by-diff'] = calcWinDiff(dataObj['home-game'], dataObj['score-diff'])
        removeRedundantFields(dataObj)
        insertRecord(dataObj['team-name'], dataObj, data)
    open('../../db/phase3/%s.json' % year, 'w').write(json.dumps(data))


for i in range(2003, 2020):
    run(str(i))
