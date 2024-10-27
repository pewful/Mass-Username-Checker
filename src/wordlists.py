import os
import sys
from colorama import just_fix_windows_console
from src.fonts import Colorize, Center
from counters.counters import LoadCounters

def LoadWords(word_list):
    return open(f'{os.path.dirname(__file__)}/../wordlists/{word_list}').read().split()

def LoadWordlists():
    wordlist_directory = "./wordlists"
    wordlists = []

    for file_name in os.listdir(wordlist_directory):
        file = os.path.join(wordlist_directory, file_name)
        if os.path.isfile(file):
            wordlists.append(file_name)

    return wordlists

def LoadAllWordlistData(word_lists):
    Data = {}
    for list in word_lists:
        WordCount = len(LoadWords(list))
        Data[list] = WordCount
    return Data

def sortByLength(Data):
    newD = {}
    

    for k in sorted(Data, key=len, reverse=True):
        newD[k] = Data[k]
    
    return newD

def removeFinished(Data, counter):
    Unfinished = {}
    for list in Data:
        if Data[list] > counter[list]:
            Unfinished[list] = counter[list]
    return Unfinished

def AddSpacing(largest_number, current_number):
    Num = str(largest_number)
    largest_num = len(Num)
    cnum = str(current_number)

    for x in range(len(cnum), largest_num):
        cnum += " "
    return cnum

def inputScreen(OrderedList, ListData, Counter, prev_error):
    os.system('cls')
    text = Colorize("Select a wordlist", "LIGHT_GRAY")
    print(Center(text))

    c = 0
    for List in OrderedList:
        gap = ""
        Numbgap = ""
        c += 1

        OrderedListLen = len(str(len(OrderedList)))
        LenStrC = len(str(c))
        LongestWordLen = len(next(iter(OrderedList)))

        if LenStrC != OrderedList:
            Numbgap += " " * (OrderedListLen - LenStrC)
            gap += " " * ((LongestWordLen + OrderedListLen) - len(List))
        elif LenStrC == OrderedListLen:
            gap += " " * LongestWordLen - len(List)
          
        Numb = f"[{c}]"
        Numb = Numbgap + Numb

        Position = f"[- {Counter[List]} / {ListData[List]}-]"
        Position = gap + Position
        print(f"{Colorize(Numb, "BRIGHT_CYAN")}{List} {Colorize(Position, "BRIGHT_GREEN")}")

    if prev_error != None:
        print(Center(prev_error))


def InputSelection(word_lists, Services, Service):
    os.system('cls')
    just_fix_windows_console()
    prev_error = None
    ListData = LoadAllWordlistData(word_lists)
    Counter = LoadCounters(word_lists, Services, Service)
    Lists = removeFinished(ListData, Counter)
    OrderedList = sortByLength(Lists)
    Keys = list(OrderedList.keys())

    if len(word_lists) > 1:
        inputting = True
        while inputting:
            inputScreen(OrderedList, ListData, Counter, prev_error)
            selection = input("> ")
            prev_error = None
            if selection.isdigit():
                selection = int(selection) - 1
                if int(selection) > len(OrderedList):
                    prev_error = f"{Colorize("ERROR: ", "BRIGHT_RED")} \"{selection + 1}\" is out of range."
                    continue
                else:
                    print(f"{Colorize(Keys[selection], "LIGHT_GRAY")} HAS BEEN SELECTED")
                    return Keys[selection]

            if selection in Lists:
                inputting = False
                return selection

            else:
                prev_error = f'{Colorize("ERROR: ", "BRIGHT_RED")} "{selection}" is not a valid wordlist.'
    elif len(word_lists) == 1:
        return word_lists[0]
    else:
        print(f'{Colorize("ERROR: ", "BRIGHT_RED")} No wordlists.')
        print("Drop wordlists into the wordlists folder. Each word should be seperated by a new line.")
        exit()