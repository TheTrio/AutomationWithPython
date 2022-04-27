# Program to find the most used word(and how many times it was used) by users
# in a Discord channel
import json
from collections import Counter
import re

# data.json has the data for the discord channel.
# To generate it, use https://github.com/Tyrrrz/DiscordChatExporter

with open("data.json", encoding="utf-8") as f:
    # Using UTF-8 since a lot of messages contain emojis and other non ascii characters
    data = json.load(f)

d = {}
for message in data["messages"]:
    if message["author"]["name"] not in d:
        words = re.split(r"\s+", message["content"])
        # Using the re.split instead of the usual string.split to avoid empty words
        d[message["author"]["name"]] = Counter(words)
    else:
        d[message["author"]["name"]].update(words)

values = []
keys = []
for k, v in d.items():
    keys.append(k)
    # All this probably could be done using a list comprehension but I wasn't
    # sure if d.keys() has the same order as d.values()
    values.append(v.most_common(1)[0])
    # Besides, that might even be dependent on the python version.
    # If it isn't, this could be replaced with a one liner

# sorting using the number of times the most used word was used
values, keys = zip(*sorted(zip(values, keys), key=lambda x: x[0][1], reverse=True))

with open("Data.txt", "w", encoding="utf-8") as f:
    for v, k in zip(values, keys):
        f.write(f'{k},"{str(v[0])}" {str(v[1])} number of times\n')
