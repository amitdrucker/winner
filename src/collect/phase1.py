# -*- coding: utf-8 -*-
# 2003 - 2019

import base64
import json
import re

import httplib2
import sys
from bs4 import BeautifulSoup

ROOT_URL = 'https://basket.co.il/'
yearUrl = ROOT_URL + 'results.asp?cYear=%s'
h = httplib2.Http()


def encodeHebrew(val):
    return base64.b64encode(val.encode('UTF-8'))


def decodeHebrew(val):
    return base64.b64decode(val)


def getScoreDiff(val):
    val = re.sub('\([^)]\)', '', val)
    return eval(re.sub('[^0-9\-]', '', val)) * -1


def getScore(val, home):
    index = 1 if home else 0
    val = re.sub('\([^)]\)', '', val)
    return int(re.sub('[^0-9\-]', '', val).split('-')[index])


def convertToInt(val):
    try:
        return int(val)
    except:
        return 0


def enrichWithQuarters(soup, dataObj):
    quartersScore = soup.find('table', class_='stats_tbl categories')
    quartersScore = quartersScore.findAll('td',
                                          class_=['td_odd td_data da_ltr_center', 'td_even td_data da_ltr_center'])
    dataObj['hq1'] = int(quartersScore[0].text)
    dataObj['hq2'] = int(quartersScore[1].text)
    dataObj['hq3'] = int(quartersScore[2].text)
    dataObj['hq4'] = int(quartersScore[3].text)
    dataObj['aq1'] = int(quartersScore[4].text)
    dataObj['aq2'] = int(quartersScore[5].text)
    dataObj['aq3'] = int(quartersScore[6].text)
    dataObj['aq4'] = int(quartersScore[7].text)


def enrichWithMainStats(soup, dataObj, isHome):
    index = 2 if isHome else 3
    prefixLetter = 'h' if isHome else 'a'
    table = soup.findAll('table', class_='stats_tbl')[index]
    rows = table.findAll('tr', class_=['row even', 'row odd'])[1:-1]
    counter = 1
    for row in rows:
        columns = row.findAll('td', class_='da_ltr_center')
        dataObj[prefixLetter + 'p' + str(counter) + '-open'] = columns[0].text == '*'
        dataObj[prefixLetter + 'p' + str(counter) + '-minutes'] = convertToInt(columns[1].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-points'] = convertToInt(columns[2].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-2pts-made'] = convertToInt(columns[3].text.split('/')[0])
        dataObj[prefixLetter + 'p' + str(counter) + '-2pts-total'] = convertToInt(columns[3].text.split('/')[1])
        dataObj[prefixLetter + 'p' + str(counter) + '-3pts-made'] = convertToInt(columns[5].text.split('/')[0])
        dataObj[prefixLetter + 'p' + str(counter) + '-3pts-total'] = convertToInt(columns[5].text.split('/')[1])
        dataObj[prefixLetter + 'p' + str(counter) + '-fts-made'] = convertToInt(columns[7].text.split('/')[0])
        dataObj[prefixLetter + 'p' + str(counter) + '-fts-total'] = convertToInt(columns[7].text.split('/')[1])
        dataObj[prefixLetter + 'p' + str(counter) + '-def-reb'] = convertToInt(columns[9].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-off-reb'] = convertToInt(columns[10].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-fouls-committed'] = convertToInt(columns[12].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-fouls-received'] = convertToInt(columns[13].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-steals'] = convertToInt(columns[14].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-turnovers'] = convertToInt(columns[15].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-assists'] = convertToInt(columns[16].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-blocks-committed'] = convertToInt(columns[17].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-blocks-received'] = convertToInt(columns[18].text)
        dataObj[prefixLetter + 'p' + str(counter) + '-dunks'] = convertToInt(columns[19].text)
        # dataObj[prefixLetter + 'p' + str(counter) + '-rating'] = convertToInt(columns[20].text)
        # dataObj[prefixLetter + 'p' + str(counter) + '-plusminus'] = convertToInt(columns[21].text)
        counter += 1


def enrichWithAdditionalStats(soup, dataObj, isHome):
    index = 4 if isHome else 5
    prefixLetter = 'h' if isHome else 'a'
    table = soup.findAll('table', class_='stats_tbl')[index]
    rows = table.findAll('tr', class_=['row even', 'row odd'])[2:]
    playerOrigin = None
    for row in rows:
        playerOrigin = 'israeli' if not playerOrigin else 'foreign'
        columns = row.findAll('td', class_='da_ltr_center')
        dataObj[prefixLetter + playerOrigin + '-minutes'] = convertToInt(columns[0].text)
        dataObj[prefixLetter + playerOrigin + '-points'] = convertToInt(columns[1].text)
        dataObj[prefixLetter + playerOrigin + '-2pts-made'] = convertToInt(columns[2].text.split('/')[0])
        dataObj[prefixLetter + playerOrigin + '-2pts-total'] = convertToInt(columns[2].text.split('/')[1])
        dataObj[prefixLetter + playerOrigin + '-3pts-made'] = convertToInt(columns[4].text.split('/')[0])
        dataObj[prefixLetter + playerOrigin + '-3pts-total'] = convertToInt(columns[4].text.split('/')[1])
        dataObj[prefixLetter + playerOrigin + '-fts-made'] = convertToInt(columns[6].text.split('/')[0])
        dataObj[prefixLetter + playerOrigin + '-fts-total'] = convertToInt(columns[6].text.split('/')[1])
        dataObj[prefixLetter + playerOrigin + '-def-reb'] = convertToInt(columns[8].text)
        dataObj[prefixLetter + playerOrigin + '-off-reb'] = convertToInt(columns[9].text)
        dataObj[prefixLetter + playerOrigin + '-fouls-committed'] = convertToInt(columns[11].text)
        dataObj[prefixLetter + playerOrigin + '-fouls-received'] = convertToInt(columns[12].text)
        dataObj[prefixLetter + playerOrigin + '-steals'] = convertToInt(columns[13].text)
        dataObj[prefixLetter + playerOrigin + '-turnovers'] = convertToInt(columns[14].text)
        dataObj[prefixLetter + playerOrigin + '-assists'] = convertToInt(columns[15].text)
        dataObj[prefixLetter + playerOrigin + '-blocks-committed'] = convertToInt(columns[16].text)
        dataObj[prefixLetter + playerOrigin + '-blocks-received'] = convertToInt(columns[17].text)
        dataObj[prefixLetter + playerOrigin + '-dunks'] = convertToInt(columns[18].text)
        # dataObj[prefixLetter + playerOrigin + '-rating'] = convertToInt(columns[19].text)


def enrichWithTotalWinsAndPoints(currentData):
    statsPerTeam = {}
    for dataObj in currentData:
        home = dataObj['home']
        away = dataObj['away']
        if home not in statsPerTeam:
            statsPerTeam[home] = {
                'homeTotalGames': 0,
                'homeWonGames': 0,
                'homeTotalPointsCommitted': 0,
                'homeTotalPointsReceived': 0,
                'awayTotalGames': 0,
                'awayWonGames': 0,
                'awayTotalPointsCommitted': 0,
                'awayTotalPointsReceived': 0
            }
        if away not in statsPerTeam:
            statsPerTeam[away] = {
                'homeTotalGames': 0,
                'homeWonGames': 0,
                'homeTotalPointsCommitted': 0,
                'homeTotalPointsReceived': 0,
                'awayTotalGames': 0,
                'awayWonGames': 0,
                'awayTotalPointsCommitted': 0,
                'awayTotalPointsReceived': 0
            }
        statsPerTeam[home]['homeTotalGames'] += 1
        if dataObj['scoreDiff'] > 0:
            statsPerTeam[home]['homeWonGames'] += 1
        statsPerTeam[home]['homeTotalPointsCommitted'] += dataObj['homeScore']
        statsPerTeam[home]['homeTotalPointsReceived'] += dataObj['awayScore']

        statsPerTeam[away]['awayTotalGames'] += 1
        if dataObj['scoreDiff'] < 0:
            statsPerTeam[away]['awayWonGames'] += 1
        statsPerTeam[away]['awayTotalPointsCommitted'] += dataObj['awayScore']
        statsPerTeam[away]['awayTotalPointsReceived'] += dataObj['homeScore']

        dataObj['hhomeTotalGames'] = statsPerTeam[home]['homeTotalGames']
        dataObj['hhomeWonGames'] = statsPerTeam[home]['homeWonGames']
        dataObj['hhomeTotalPointsCommitted'] = statsPerTeam[home]['homeTotalPointsCommitted']
        dataObj['hhomeTotalPointsReceived'] = statsPerTeam[home]['homeTotalPointsReceived']
        dataObj['hawayTotalGames'] = statsPerTeam[home]['awayTotalGames']
        dataObj['hawayWonGames'] = statsPerTeam[home]['awayWonGames']
        dataObj['hawayTotalPointsCommitted'] = statsPerTeam[home]['awayTotalPointsCommitted']
        dataObj['hawayTotalPointsReceived'] = statsPerTeam[home]['awayTotalPointsReceived']

        dataObj['ahomeTotalGames'] = statsPerTeam[away]['homeTotalGames']
        dataObj['ahomeWonGames'] = statsPerTeam[away]['homeWonGames']
        dataObj['ahomeTotalPointsCommitted'] = statsPerTeam[away]['homeTotalPointsCommitted']
        dataObj['ahomeTotalPointsReceived'] = statsPerTeam[away]['homeTotalPointsReceived']
        dataObj['aawayTotalGames'] = statsPerTeam[away]['awayTotalGames']
        dataObj['aawayWonGames'] = statsPerTeam[away]['awayWonGames']
        dataObj['aawayTotalPointsCommitted'] = statsPerTeam[away]['awayTotalPointsCommitted']
        dataObj['aawayTotalPointsReceived'] = statsPerTeam[away]['awayTotalPointsReceived']


def scrapeRow(currentData, row, round):
    columns = row.findAll('td')
    dataObj = {
        'round': round,
        'date': columns[0].text,
        'home': encodeHebrew(columns[5].text),
        'homeScore': getScore(columns[8].text, True),
        'away': encodeHebrew(columns[6].text),
        'awayScore': getScore(columns[8].text, False),
        'scoreDiff': getScoreDiff(columns[8].text)
    }
    link = ROOT_URL + columns[7].find('a')['href'].replace('#!review', '')
    resp, content = h.request(link)
    soup = BeautifulSoup(content, 'html.parser')
    enrichWithQuarters(soup, dataObj)
    enrichWithMainStats(soup, dataObj, True)
    enrichWithMainStats(soup, dataObj, False)
    enrichWithAdditionalStats(soup, dataObj, True)
    enrichWithAdditionalStats(soup, dataObj, False)
    currentData.append(dataObj)


def run(year):
    print 'working on year %s' % year
    print '--------------------'
    currentData = []
    resp, content = h.request(yearUrl % year)
    soup = BeautifulSoup(content, 'html.parser')
    counter = 1
    round = 1
    for row in soup.findAll("tr"):
        if 'class' in row.attrs:
            if row['class'][0] == 'row' and row['class'][1] in 'oddeven':
                scrapeRow(currentData, row, round)
                print 'iteration %s' % str(counter)
                counter += 1
        elif row.td and 'class' in row.td.attrs and row.td['class'][0] == 'round_break':
            round = int(re.sub('[^0-9]', '', row.td.text))
            print 'round %s' % str(round)
    enrichWithTotalWinsAndPoints(currentData)
    print 'saving year %s' % year
    open('../../db/phase1/%s.json' % year, 'w').write(json.dumps(currentData))


if len(sys.argv) == 2:
    print 'running only for year %s' % str(sys.argv[1])
    run(str(sys.argv[1]))
else:
    for i in range(2003, 2020):
        run(str(i))
