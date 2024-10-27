import json
from pathlib import Path
counter_path = "./counters/"

def GenerateCounters(Services):
    Dict = {}
    for Service in Services:
        my_file = Path(f"{counter_path}{Service}.json")

        if not my_file.is_file():
            with open(my_file, "w") as outfile:
                outfile.write(json.dumps(Dict))

def LoadCounters(wordlists, Services, Service):
    GenerateCounters(Services)
    counter_obj = open(f"{counter_path}{Service}.json")
    counters = json.load(counter_obj)
    
    for word in wordlists:
        if word not in counters:
            counters[word] = 0

    to_delete = []

    for count in counters:
        if count not in wordlists:
            to_delete.append(count)

    for key in to_delete:
        counters.pop(key, None)

    return counters

def SaveCounters(counter, Service):
    my_file = Path(f"{counter_path}{Service}.json")

    if my_file.is_file():
        with open(f"{counter_path}{Service}.json", 'w') as save_file:
            json.dump(counter, save_file)
        return
    else:
        print("ERROR WRITING COUNTER")
        exit()

def GetCounterPos(counter, wordlist_selection):
    return counter[wordlist_selection]