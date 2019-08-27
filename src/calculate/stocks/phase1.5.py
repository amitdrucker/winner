import json

data = []
for year in range(2015, 2020):
    data = data + json.loads(open('data/phase2/%s.json' % year, 'r').read())
    open('data/phase2/result.json', 'w').write(json.dumps(data))
