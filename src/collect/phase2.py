import json


def normalizeDate(date):
    date = date.strip()
    if len(date) == 10:
        return date + '00:00'
    return date


def run(year):
    data = []
    currentPhase1Data = json.loads(open('../../db/phase1/%s.json' % year, 'r').read())
    for dataObj in currentPhase1Data:
        homeTeamObj = {'date': normalizeDate(dataObj['date']),
                       'round': dataObj['round'],
                       'team-name': dataObj['home'],
                       'home-game': True,
                       'team-score': dataObj['homeScore'],
                       'opponent-score': dataObj['awayScore'],
                       'score-diff': dataObj['scoreDiff']}
        for key, value in dataObj.iteritems():
            if key.startswith('h') and key != 'homeScore' \
                    and key != 'home':
                homeTeamObj[key[1:]] = value
        data.append(homeTeamObj)

        awayTeamObj = {'date': normalizeDate(dataObj['date']),
                       'round': dataObj['round'],
                       'team-name': dataObj['away'],
                       'home-game': False,
                       'team-score': dataObj['awayScore'],
                       'opponent-score': dataObj['homeScore'],
                       'score-diff': dataObj['scoreDiff']}
        for key, value in dataObj.iteritems():
            if key.startswith('a') and key != 'awayScore' \
                    and key != 'away':
                awayTeamObj[key[1:]] = value
        data.append(awayTeamObj)
    open('../../db/phase2/%s.json' % year, 'w').write(json.dumps(data))


for i in range(2003, 2020):
    run(str(i))
