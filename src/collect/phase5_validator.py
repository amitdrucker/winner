import json


def print_all_is_won(obj):
    print obj['home_score-diff-avg']
    for j in range(-12, 13):
        print 'away ' + str(j) + ': ' + str(obj['away_is-won_' + str(j)])
    for j in range(-12, 13):
        print 'home ' + str(j) + ': ' + str(obj['home_is-won_' + str(j)])
    exit(0)


phase5Data = json.loads(open('../../db/phase5/result.json', 'r').read())
for entry in phase5Data:
    if entry['away_round'] != entry['away_round']:
        print 'round error!\n' + json.dumps(entry)
    if entry['away_date'] != entry['away_date']:
        print 'round error!\n' + json.dumps(entry)
    # for key in entry.keys():
    #     if 'away_is-won' in key and 'avg' not in key:
    #         away_is_won = entry[key]
    #         home_is_won = entry[key.replace('away', 'home')]
    #         if away_is_won != (not home_is_won) and :
    #             print key + ' error'
    #             print_all_is_won(entry)
    # if entry['away_win-by-diff'] != 9 - entry['away_win-by-diff']:
    # print 'win-by-diff error!\n' + json.dumps(entry)
    # print 'away_win-by-diff: %s, away_win-by-diff: %s' % (entry['away_win-by-diff'], entry['away_win-by-diff'] * -1)
    # if entry['away_date'] != entry['away_date']:
    #     print 'round error!\n' + json.dumps(entry)
