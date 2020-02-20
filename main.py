import json
from collections import Counter
import collections
import matplotlib.pyplot as plt
import re
from helpers import parse_obj

MESSAGES_PATH = "message_1.json"

with open(MESSAGES_PATH) as f:
    data = json.load(f, object_hook=parse_obj)

types = Counter()
messages = data["messages"]

for msg in messages:
    types[msg["type"]] += 1

participants = list()
for part in data["participants"]:
    splitted = part["name"].split(" ")
    participants.append((splitted[0], splitted[1]))

regexp = re.compile(r".*[xX]([dD])+.*")
re_name = re.compile(r"@(?P<imie>\w+)\s(?P<nazwisko>\w+)")
people = Counter()
photos = Counter()
xds = Counter()
reactions = Counter()
smiles = Counter()
given_reactions = Counter()
characters = Counter()
likes = Counter()
mentions = Counter()
total_messages = types["Generic"] + types["Share"]
for msg in messages:
    typee = msg["type"]
    if "reactions" in msg:
        reactions[msg["sender_name"]] += len(msg["reactions"])

        for reaction in msg["reactions"]:
            given_reactions[reaction["actor"]] += 1
            if reaction["reaction"] == "😆":
                smiles[reaction["actor"]] += 1

    if "content" in msg:
        characters[msg["sender_name"]] += len(msg["content"])
        if regexp.search(msg["content"]):
            xds[msg["sender_name"]] += 1
        matches = re_name.findall(msg["content"])
        if len(matches) != 0:
            if matches[0] in participants:
                mentions[matches[0][0] + " " + matches[0][1]] += 1

    if "photos" in msg:
        photos[msg["sender_name"]] += 1
    if typee == "Generic" or typee == "Share":
        people[msg["sender_name"]] += 1

stos = dict()
for person, count in people.items():
    if count != 0 and characters[person] != 0:
        stos[person] = characters[person] / count

sorted_dict = {k: v for k, v in sorted(stos.items(), key=lambda item: item[1])}

new = photos.most_common(10)
# new = sorted_dict
keys, vals = list(zip(*new))
# print(sorted_dict)
# keys = list(sorted_dict.keys())
# vals = list(sorted_dict.values())

fig, ax = plt.subplots()
for i, v in enumerate(vals):
    ax.text(v + 1, i - 0.25, v)

print(mentions)
plt.barh(keys, vals)
plt.title("xd")
plt.ylabel("Pierwsza 10")
plt.show()

