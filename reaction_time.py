import json
from collections import Counter


data = None
with open("valid1.json") as f:
    data = json.load(f)


people = Counter()
avg_time = Counter()


for key, msg in data.items():
    people[msg["msg_sender"]] +=1
    delta = int(msg["msg_timestamp"]) - int(msg["email_timestamp"][0])
    avg_time[msg["msg_sender"]] += delta

for person, avg in zip(people.items(), avg_time.items()):
    print(f"{person[0]}: {avg[1]/person[1]}")