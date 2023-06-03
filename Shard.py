import Manager
import math
import random
import copy

def init():
    #DeclareVariables
    global average_power
    average_power = 50
    global average_cost
    average_cost = 80
    global correction
    correction = 0.2
    global special_correction
    special_correction = 0.4
    global min_cost
    min_cost = 1
    global max_cost
    max_cost = 300
    global bugged_list
    bugged_list = [
        "Shadowtracer",
        "Beastguard",
        "WildScratch",
        "Healing",
        "Sacredshade",
        "ChangeBunny"
    ]
    global special_list
    special_list = [
        "Jackpot",
        "WildScratch",
        "ChangeBunny",
        "Voidlay",
        "Tornadoslicer",
        "Chiselbalage",
        "TissRosain",
        "FoldingTurb"
    ]
    global skip_list
    skip_list = [
        "Bloodsteel",
        "SummonChair",
        "Demoniccapture",
        "Accelerator",
        "AccelWorld",
        "Beastguard",
        "Shadowtracer",
        "Sacredshade",
        "Reflectionray",
        "Aquastream",
        "Dimensionshift",
        "GoldBarrett",
        "Aimingshield",
        "CurseDray",
        "Petrey",
        "PetraBless",
        "Acidgouache",
        "Venomsmog"
    ]

def set_default_shard_power():
    #Recalculate default shard power in a more convenient way for balance
    for entry in Manager.datatable["PB_DT_ShardMaster"]:
        if not entry in Manager.mod_data["ShardBase"]:
            continue
        base = Manager.datatable["PB_DT_ShardMaster"][entry]["useMP"] * Manager.mod_data["ShardBase"][entry]["Base"]
        if entry in skip_list or entry == "Healing":
            balance = 1.0
        elif entry in special_list:
            balance = (average_power/base)**correction
        else:
            balance = (average_cost/Manager.datatable["PB_DT_ShardMaster"][entry]["useMP"])**correction
        Manager.datatable["PB_DT_ShardMaster"][entry]["minGradeValue"] = round(base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][entry]["maxGradeValue"] = round(base * balance * Manager.mod_data["ShardBase"][entry]["Grade"], 3)

def randomize_shard_power(scale):
    for entry in Manager.datatable["PB_DT_ShardMaster"]:
        #Only randomize shards that have an entry in shard base
        if not entry in Manager.mod_data["ShardBase"]:
            continue
        if entry in skip_list or entry == "LigaDoin":
            continue
        original_cost      = int(Manager.datatable["PB_DT_ShardMaster"][entry]["useMP"])
        original_doin_cost = int(Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"])
        #Reduce the range for certain shards
        if entry in bugged_list:
            reduction = 6
        elif entry in special_list:
            reduction = 3
        else:
            reduction = 1
        #Randomize magic cost first
        multiplier = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 3)/original_cost
        Manager.datatable["PB_DT_ShardMaster"][entry]["useMP"] = int(original_cost * multiplier)
        #Riga Doin explosion is shared with Riga Storeama
        if entry == "LigaStreyma":
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"] = int(original_doin_cost * multiplier)
        #Randomize power based on magic cost
        if scale:
            new_cost      = Manager.datatable["PB_DT_ShardMaster"][entry]["useMP"]
            new_doin_cost = Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["useMP"]
        else:
            multiplier    = Manager.random_weighted(original_cost, min_cost, int(max_cost/reduction), 1, 3)/original_cost
            new_cost      = int(original_cost * multiplier)
            new_doin_cost = int(original_doin_cost * multiplier)
        new_base = new_cost * Manager.mod_data["ShardBase"][entry]["Base"]
        #Prevent power from scaling too high or too low
        if entry == "Healing":
            balance = 1.0
        elif entry in special_list:
            balance = (1/(multiplier**special_correction))*(average_power/new_base)**correction
        else:
            balance = (average_cost/new_cost)**correction
        Manager.datatable["PB_DT_ShardMaster"][entry]["minGradeValue"] = round(new_base * balance, 3)
        Manager.datatable["PB_DT_ShardMaster"][entry]["maxGradeValue"] = round(new_base * balance * Manager.mod_data["ShardBase"][entry]["Grade"], 3)
        #Riga Doin explosion is shared with Riga Storeama
        if entry == "LigaStreyma":
            new_doin_base = new_doin_cost * Manager.mod_data["ShardBase"]["LigaDoin"]["Base"]
            balance       = (average_cost/new_doin_cost)**correction
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["minGradeValue"] = round(new_doin_base * balance, 3)
            Manager.datatable["PB_DT_ShardMaster"]["LigaDoin"]["maxGradeValue"] = round(new_doin_base * balance * Manager.mod_data["ShardBase"]["LigaDoin"]["Grade"], 3)

def update_special_properties():
    #A few shards have a multiplier different than 1.0 in DamageMaster so update their shard power based on that
    for data in ["minGradeValue", "maxGradeValue"]:
        Manager.datatable["PB_DT_ShardMaster"]["DragonicRage"][data] = round(Manager.datatable["PB_DT_ShardMaster"]["DragonicRage"][data] / 1.45, 3)
        Manager.datatable["PB_DT_ShardMaster"]["SummonAme"][data]    = round(Manager.datatable["PB_DT_ShardMaster"]["SummonAme"][data]    / 0.75, 3)

def rescale_level_based_shards():
    #Money is Power and Red Rememberance only take starting stats and level up stats in account
    #So considerably increase their multipliers to make them useful if level 1 capped
    Manager.datatable["PB_DT_CoordinateParameter"]["P0000_MONEYISPOWER_ATTACK_RATE_MAX"]["Value"] = 0.5
    #Unfortunately Red Rememberance seems to be capped at 1.0
    Manager.datatable["PB_DT_ShardMaster"]["RedDowther"]["minGradeValue"] = 0.5
    Manager.datatable["PB_DT_ShardMaster"]["RedDowther"]["maxGradeValue"] = 1.0