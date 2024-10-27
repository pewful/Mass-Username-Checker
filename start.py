import asyncio
import aiohttp
import random
import os
from os import system
from src import wordlists, request
from src.fonts import Colorize, Center
from counters import counters
from config import config 

Services = []
config_file = config.LoadConfig()
word_lists = wordlists.LoadWordlists()

for item in config_file:
    if item == "proxy":
        continue
    Services.append(item)

def ContainsSpecial(Username, Service):
    special_characters = config_file[Service]

    if any(c in special_characters for c in Username):
        return True
    else:
        return False
    
def TooShortOrLong(Username, Service):
    username_length = len(Username)
    conf = config_file[Service]

    if username_length < conf["shortest_username"]:
        return True
    if username_length > conf["longest_username"]:
        return True
    else:
        return False
    
def WordlistMenu(Services, Service):
    if "wordlist" in config_file:
        wordlist_selection = config_file["wordlist"]
    else:
        wordlist_selection = wordlists.InputSelection(word_lists, Services, Service)
    return wordlist_selection

def SaveName(Username, Wordlist, Service):
    FilePath = f"./output/{Service}"
    if not os.path.isdir(FilePath):
        os.makedirs(FilePath)

    with open(f"{FilePath}/{Wordlist}", "a+") as outfile:
        outfile.write("%s\n" % Username)

def ServiceSelectonUI(Errors = None):
    os.system("cls")
    Title = "Select a service"
    Title = Colorize(Title, "LIGHT_GRAY")
    Title = Center(Title)

    print(Title)

    if Errors != None:
        print(f"{Colorize("ERROR: ", "BRIGHT_RED")}{Errors}")

    Count = 0
    for Service in Services:
        Count+=1
        Option = f"[{Count}]"
        Option = Colorize(Option, "BRIGHT_CYAN")
        print(f"{Option}{Service}")

def ServiceSelection():
    Errors = None
    Choice = None

    while Choice == None:
        ServiceSelectonUI(Errors)
        selection_choice = input("> ")
        if selection_choice.isdigit():
            selection_choice = int(selection_choice) - 1
            if selection_choice > len(Services):
                Errors = "Out of range"
                continue
            else:
                Choice = Services[selection_choice]
        else:
            if any(selection_choice in s for s in Services):
                Choice = selection_choice
            else:
                Errors = f"{selection_choice} is not an available service."
    return Choice

Service = ServiceSelection()
system(f"title {Service}")
counter = counters.LoadCounters(word_lists, Services, Service)
wordlist_selection = WordlistMenu(Services, Service)
words = wordlists.LoadWords(wordlist_selection)
system(f"title {Service} - {wordlist_selection}")
            
def UpdateTitle(Service):
    system(f"title {Service} - {wordlist_selection}     [{counter[wordlist_selection]} / {len(words)}]")

def CreateTasks(Session, index_of_word, Threads, Service):
    tasks = []
    word_list_length = len(words)
    if index_of_word + Threads > word_list_length - Threads:
        Threads = word_list_length - index_of_word
    elif Threads == 0:
        print(f"{Colorize("FINISHED LIST", "BRIGHT_BLUE")}")
        exit()
    
    for index in range(index_of_word, index_of_word + Threads):
        username = words[index]
        contains_special = ContainsSpecial(username, Service)

        if contains_special:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Username contains special characters")
            continue

        username_length_test = TooShortOrLong(username, Service)

        if username_length_test:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Too many or too few characters in username")
            continue
        
        if Service == "Discord":
            tasks.append(request.CheckDiscordUsername(Session, username, config_file['proxy']))
            continue
        if Service == "Roblox":
            tasks.append(request.CheckRobloxUsername(Session, username, config_file['proxy']))
            continue
        if Service == "Linktree":
            tasks.append(request.CheckLinktreeUsername(Session, username, config_file['proxy']))
            continue
        if Service == "Discord Vanity":
            tasks.append(request.CheckDiscordVanity(Session, username, config_file['proxy']))
            continue
        if Service == "Minecraft":
            tasks.append(request.CheckMinecraftUsername(Session, username))
            continue
        if Service == "Github":
            tasks.append(request.CheckGithubUsername(Session, username, config_file['proxy']))
            continue

        if len(tasks) == 0:
            return False
    return tasks

def LinktreeResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection")
            print(config_file['proxy'])
        elif type(response) is not int:
            if response["result"] == "fail":
                print(f"{Colorize(response["Username"], "RED")} has been taken already.")
            elif response["result"] == "success":
                print(f"{Colorize(response['Username'], "GREEN")} is available!")
                SaveName(response['Username'], wordlist_selection, Service)

            counter[wordlist_selection] +=1
            UpdateTitle(Service)
            counters.SaveCounters(counter, Service)

async def DiscordResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            sleep_time = random.randint(3, 9)
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection. Sleeping for: {sleep_time}")
            await asyncio.sleep(sleep_time)
        elif "global" in response:
            sleep_time = random.randint(3, 9)
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection. Sleeping for: {sleep_time}")
            await asyncio.sleep(sleep_time)
            continue
        else:
            if "code" in response:
                if response["code"] == 50035:
                    print(f"{Colorize("ERROR: ", "RED")} Invalid username")

            elif "taken" in response:
                if response["taken"]:
                    print(f"{Colorize(response["Username"], "RED")} has been taken already.")
                elif not response["taken"]:
                    print(f"{Colorize(response['Username'], "GREEN")} is available!")
                    SaveName(response['Username'], wordlist_selection, Service)
                
                counter[wordlist_selection] +=1
                UpdateTitle(Service)
                counters.SaveCounters(counter, Service)
    return

def RobloxResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection")
        elif response != None:
            if response['taken']:
                print(f"{Colorize(response["Username"], "RED")} has been taken already.")
            elif not response['taken']:
                print(f"{Colorize(response['Username'], "GREEN")} is available!")
                SaveName(response['Username'], wordlist_selection, Service)

            counter[wordlist_selection] +=1
            UpdateTitle(Service)
            counters.SaveCounters(counter, Service)
        elif response == None:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection")
            continue

def DiscordVanityResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection")
        elif response != None:
            if not response['code'] == 10006:
                print(f"{Colorize(response['Vanity'], "GREEN")} is valid!")
                SaveName(response['Vanity'], wordlist_selection, Service)
            else:
                print(f"{Colorize(response["Vanity"], "RED")} is not a valid invite")
            
            counter[wordlist_selection] += 1
            UpdateTitle(Service)
            counters.SaveCounters(counter, Service)
        elif response == None:
            print(response)
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Proxy connection")
            continue

def MinecraftResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Rate Limited")
        elif response != None:
            if 'path' in response:
                print(f"{Colorize(response['Username'], "GREEN")} is available!")
                SaveName(response['Username'], wordlist_selection, Service)
            elif 'id' in response:
                print(f"{Colorize(response["Username"], "RED")} has been taken already.")
            
            counter[wordlist_selection] += 1
            UpdateTitle(Service)
            counters.SaveCounters(counter, Service)
            
def GithubResponse(responses, Service):
    for response in responses:
        if type(response) is int:
            print(f"{Colorize("ERROR: ", "BRIGHT_RED")} Rate Limited")
        else:
            if "div" in response:
                print(f"{Colorize("Taken", "RED")}")
            else:
                if "available" in response:
                    Username = response.split(" ")[0]
                    print(f"{Colorize(Username, "GREEN")} is available!")
                    SaveName(Username, wordlist_selection, Service)

            counter[wordlist_selection] += 1
            UpdateTitle(Service)
            counters.SaveCounters(counter, Service)

async def main():
    loop = asyncio.get_running_loop()
    threads = 1
    if Service == "Minecraft":
        threads = 1

    async with aiohttp.ClientSession() as Session:
        while counter[wordlist_selection] != len(words):
            tasks = CreateTasks(Session, counter[wordlist_selection], threads, Service)
            if not tasks:
                counter[wordlist_selection] = counter[wordlist_selection] + threads
                continue
            else:
                responses = await asyncio.gather(*tasks)

                if Service == "Linktree":
                    LinktreeResponse(responses, Service)
                    continue
                if Service == "Discord":
                    await DiscordResponse(responses, Service)
                    continue
                if Service == "Roblox":
                    RobloxResponse(responses, Service)
                    continue
                if Service == "Discord Vanity":
                    DiscordVanityResponse(responses, Service)
                    continue
                if Service == "Minecraft":
                    MinecraftResponse(responses, Service)
                    await asyncio.sleep(3.5)
                    continue
                if Service == "Github":
                    GithubResponse(responses, Service)
                    continue
asyncio.run(main())