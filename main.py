import json
from collections import Counter
import collections
import matplotlib.pyplot as plt
import re
from helpers import parse_obj
from stats import messenger_stats

MESSAGES_PATH = "message_1.json"

with open(MESSAGES_PATH) as f:
    data = json.load(f, object_hook=parse_obj)

sttt = json.dumps(data)

with open("good_json.json", "w") as f:
    f.write(sttt)


stats = messenger_stats.MessengerStats(data)
stats.run()


# re_name = re.compile(r"@(?P<imie>\w+)\s(?P<nazwisko>\w+)")
# people = Counter()
# photos = Counter()
# xds = Counter()
# reactions = Counter()
# smiles = Counter()
# given_reactions = Counter()
# characters = Counter()
# likes = Counter()
# mentions = Counter()
# total_messages = types["Generic"] + types["Share"]
# for msg in messages:
#     typee = msg["type"]
#     if "reactions" in msg:
#         reactions[msg["sender_name"]] += len(msg["reactions"])
#
#         for reaction in msg["reactions"]:
#             given_reactions[reaction["actor"]] += 1
#             if reaction["reaction"] == "😆":
#                 smiles[reaction["actor"]] += 1
#
#     if "content" in msg:
#         characters[msg["sender_name"]] += len(msg["content"])
#         if regexp.search(msg["content"]):
#             xds[msg["sender_name"]] += 1
#         matches = re_name.findall(msg["content"])
#         if len(matches) != 0:
#             if matches[0] in participants:
#                 mentions[matches[0][0] + " " + matches[0][1]] += 1
#
#     if "photos" in msg:
#         photos[msg["sender_name"]] += 1
#     if typee == "Generic" or typee == "Share":
#         people[msg["sender_name"]] += 1
#
# stos = dict()
# for person, count in people.items():
#     if count != 0 and characters[person] != 0:
#         stos[person] = characters[person] / count
#
