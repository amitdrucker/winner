import json

phase5Data = json.loads(open('../../db/phase5/result.json', 'r').read())
for entry in phase5Data:
    if entry['home_round'] != entry['away_round']:
        print 'round error!\n' + json.dumps(entry)
    if entry['home_date'] != entry['away_date']:
        print 'round error!\n' + json.dumps(entry)
    if entry['home_is-won'] != (not entry['away_is-won']):
        print 'is won error!\n' + json.dumps(entry)
    if entry['home_win-by-diff'] != 9 - entry['away_win-by-diff']:
        # print 'win-by-diff error!\n' + json.dumps(entry)
        print 'home_win-by-diff: %s, away_win-by-diff: %s' % (entry['home_win-by-diff'], entry['away_win-by-diff'] * -1)
        if entry['home_date'] != entry['away_date']:
            print 'round error!\n' + json.dumps(entry)
