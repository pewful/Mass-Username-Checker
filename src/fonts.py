import random
import os 

Colors = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "LIGHT_GRAY": "\033[37m",
    "DARK_GRAY": "\033[90m",
    "BRIGHT_RED": "\033[91m",
    "BRIGHT_GREEN": "\033[92m",
    "BRIGHT_YELLOW": "\033[93m",
    "BRIGHT_BLUE": "\033[94m",
    "BRIGHT_MAGENTA": "\033[95m",
    "BRIGHT_CYAN": "\033[96m",
    "WHITE": "\033[97m",
}

RESET = '\033[0m'

def GetRandomColor():
    return random.choice(list(Colors.keys()))

def Colorize(String, Color = "Random"):
    color = Color
    if Color == "Random":
        color = GetRandomColor()
    return(f"{Colors[color]} {String} {RESET}")

def Bolden(String):
    return(f"\033[1m{String}\033[0;0m") 

def Center(String):
    cols, rows = os.get_terminal_size()
    return("\n" + " "*(cols//2 - len(String)//2) + String)