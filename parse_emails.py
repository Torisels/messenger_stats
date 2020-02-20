import json
import re
import datetime
data = None


with open("mails.json","r") as f:
    data = json.load(f)


regex_num = re.compile(r"Łączna.*wiadomości:\s(?P<liczba>\d+)")

numbers = dict()


for key, value in data.items():
    msg = value[0].encode().decode("unicode-escape")
    print(value[1])
    try:
        if "," in value[1]:
            date_string = value[1].split(",")[1].lstrip()
        else:
            date_string = value[1]
        dt = datetime.datetime.strptime(date_string, "%d %b %Y %H:%M:%S %z")
        numbers[key] = [dt.timestamp()]
    except IndexError:
        pass


with open("timestamps.json","w") as f:
    json.dump(numbers, f)