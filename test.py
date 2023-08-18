from colorama import init, Fore, Style
init()

def print_log(info, level):
    if(level == "WARN"):
        print(Fore.YELLOW + "[WARN] " + info)
        print(Style.RESET_ALL) # Don't forget to change back to normal

print_log("This is a warning", "WARN")