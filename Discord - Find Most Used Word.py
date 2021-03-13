import json
from collections import Counter
import re
with open('data.json',encoding="utf-8") as f:
    data = json.load(f)

d = {}
for message in data['messages']:
    if message['author']['name'] not in d:
        words = re.split('\s+', message['content'])
        d[message['author']['name']] = Counter(words)
    else:
        d[message['author']['name']].update(words)

values = []
keys = []
for k,v in d.items():
    keys.append(k)
    values.append(v.most_common(1)[0])

values, keys = zip(*sorted(zip(values,keys), key=lambda x: x[0][1], reverse=True))
with open('Data.txt','w',encoding="utf-8") as f:
	for v,k in zip(values,keys):
		f.write(f'{k},"{str(v[0])}" {str(v[1])} number of times\n')