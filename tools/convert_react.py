import json

f = open('reacts')

messages = {}

for line in f.readlines():
    key,value = line.split('#',1)
    messages [key] = value.strip()

print json.dumps(messages)