import os
import json

def init():
    config = getSettings()
    API_KEY = config["API_KEY"]
    PATH = config["PATH"]
    SKYWARS_WINS = config["REQUIREMENTS"]["SKYWARS_WINS"]
    SKYWARS_LEVEL = config["REQUIREMENTS"]["SKYWARS_LEVEL"]
    BEDWARS_WINS = config["REQUIREMENTS"]["BEDWARS_WINS"]
    BEDWARS_INDEX = config["REQUIREMENTS"]["BEDWARS_INDEX"]
    BEDWARS_FKDR = config["REQUIREMENTS"]["BEDWARS_FKDR"]
    DUELS_WINS = config["REQUIREMENTS"]["DUELS_WINS"]
    DUELS_WLR = config["REQUIREMENTS"]["DUELS_WLR"]
    ARCADE_WINS = config["REQUIREMENTS"]["ARCADE_WINS"]
    MURDER_MYSTERY_WINS = config["REQUIREMENTS"]["MURDER_MYSTERY_WINS"]
    MINIMUM_GEXP = config["REQUIREMENTS"]["MINIMUM_GEXP"]
    MAXIMUM_GUILD_LEVEL = config["REQUIREMENTS"]["MAXIMUM_GUILD_LEVEL"]
    globals().update(locals())


def getSettings():
    user_home = os.path.expanduser("~")
    User_Profile = os.getenv('USERPROFILE')
    documents_path = os.path.join(user_home, 'Documents')
    folder_name = "MiscRecruitment"
    folder_path = os.path.join(documents_path, folder_name)
    file_name = "config.json"



    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

        json_data = {
            "API_KEY": "12f008e2-c1cb-4508-aef3-43f27565db1d",
            "PATH": fr'{User_Profile}\.lunarclient\offline\multiver\logs\latest.log',
            "REQUIREMENTS": {
                "SKYWARS_WINS": 0,
                "SKYWARS_LEVEL": 0,
                "BEDWARS_WINS": 0,
                "BEDWARS_INDEX": 0,
                "BEDWARS_FKDR": 0,
                "DUELS_WINS": 0,
                "DUELS_WLR": 0,
                "ARCADE_WINS": 0,
                "MURDER_MYSTERY_WINS": 0,
                "MINIMUM_GEXP": 0,
                "MAXIMUM_GUILD_LEVEL": 300
            }
        }

        with open(os.path.join(folder_path, file_name), 'w') as f:
            json.dump(json_data, f)

    with open(os.path.join(folder_path, file_name), 'r') as f:
        config = json.load(f)

    return config



