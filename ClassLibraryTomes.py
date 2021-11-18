import json
import os
import shutil
import random

is_tome = []
completion = []
count = []
log = []

#Content
with open("Data\\BookMaster\\Content\\PB_DT_BookMaster.json", "r") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\DropRateMaster\\Translation.json", "r") as file_reader:
    translation = json.load(file_reader)

for i in range(21):
    completion.append(i*5)

for i in range(21):
    if i % 2 == 0:
        is_tome.append(True)
    else:
        is_tome.append(False)
    count.append(i)

def rand_book(req, appear):
    chosen = any_pick_true(count)
    if req:
        content[21]["Value"]["RoomTraverseThreshold"] = completion[chosen]
    if appear:
        content[21]["Value"]["IslibraryBook"] = is_tome[chosen]
    i = 1
    while i <= 20:
        chosen = any_pick(count)
        if req:
            content[i]["Value"]["RoomTraverseThreshold"] = completion[chosen]
        if appear:
            content[i]["Value"]["IslibraryBook"] = is_tome[chosen]
        i += 1
    i = 1
    while i <= 21:
        if content[i]["Value"]["IslibraryBook"]:
            log_data = {}
            log_data["Key"] = translation["Value"][content[i]["Key"]]
            log_data["Value"] = {}
            log_data["Value"]["MapRequirement"] = content[i]["Value"]["RoomTraverseThreshold"]
            log.append(log_data)
        i += 1
    debug("rand_book(" + str(req) + ", " + str(appear) + ")")

def any_pick(array):
    item = random.choice(array)
    array.remove(item)
    return item
    
def any_pick_true(array):
    item = random.choice(array)
    while not is_tome[item]:
        item = random.choice(array)
    array.remove(item)
    return item

def write_patched_book():
    with open("Serializer\\PB_DT_BookMaster.json", "w") as file_writer:
        file_writer.write(json.dumps(content, indent=2))
    root = os.getcwd()
    os.chdir("Serializer")
    os.system("cmd /c UAsset2Json.exe -tobin PB_DT_BookMaster.json")
    os.chdir(root)
    shutil.move("Serializer\\PB_DT_BookMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BookMaster.uasset")
    os.remove("Serializer\\PB_DT_BookMaster.json")
    debug("write_patched_book()")

def write_book():
    shutil.copyfile("Serializer\\PB_DT_BookMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\PB_DT_BookMaster.uasset")
    debug("write_book()")

def write_book_log():
    with open("SpoilerLog\\LibraryTomes.json", "w") as file_writer:
        file_writer.write(json.dumps(log, indent=2))
    debug("write_book_log()")

def debug(line):
    file = open("SpoilerLog\\~debug.txt", "a")
    file.write("FUN " + line + "\n")
    file.close()