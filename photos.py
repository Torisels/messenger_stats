import sys
import subprocess
import os
import json
import pyautogui, time


def alt_tab(cc):
    for _ in range(cc):
        pyautogui.keyDown('alt')
        time.sleep(.2)
        pyautogui.press('tab')
        time.sleep(.2)
        pyautogui.keyUp('alt')

# from SendKeys import SendKeys
dir_path = os.path.dirname(os.path.realpath(__file__))

def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.run(["explorer", path])
path = dir_path + "\\photos\\51461709_792476117755564_3032924278858186752_n_522781301631499.png"



email_data = None
with open("timestamps.json") as f:
    email_data = json.load(f)

def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
        elif isinstance(obj[key], list):
            obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
        pass
    return obj

data = None
with open("message_1.json") as f:
    data = json.load(f, object_hook=parse_obj)

messages = data["messages"]

photo_pointer = 0
yes = 0
valid_photos = dict()
d = 0
for email_id, ts in email_data.items():
    upper_bound = ts[0] + 3600
    for index, msg in enumerate(messages):
        if "photos" in msg:
            timet = int(msg["timestamp_ms"])//1000
            if ts[0] <= timet <= upper_bound:
                for ph in msg["photos"]:
                    pp = (ph["uri"].split("/"))[-1]
                    photo_pointer += 1
                    # openImage(dir_path+"\\photos\\"+pp)
                    #
                    # answer = input("is this valid photo?: [y/n]")
                    # if answer == "y":
                    #     valid_photos[yes] = ({"email_id": email_id, "email_timestamp": ts, "photo_path": pp,
                    #                          "msg_timestamp": timet, "msg_sender": msg["sender_name"]})
                    #
                    #     # valid_photos[yes] = {"email_id": email_id, "email_date": ts, "photo_path": pp}
                    #     yes += 1
#
# with open("valid1.json", "w") as fout:
#     json.dump(valid_photos, fout)

print(photo_pointer)