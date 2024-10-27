import json
path = "./config/config.json"

def LoadConfig():
    raw_config = open(path)
    return json.load(raw_config)