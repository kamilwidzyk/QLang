import colorama

# Logger levels:
# 1. Fatal 
# 2. Error
# 3. Warning
# 4. Success
# 5. Info
# 6. Debug



# Module tags
INIT =  "INIT "
PLACE = "PLACE"

# Types
FATAL = "F", colorama.Fore.RED, colorama.Back.RESET, colorama.Style.BRIGHT, 1
ERROR = "E", colorama.Fore.RED, colorama.Back.RESET, colorama.Style.BRIGHT, 2
WARNING = "W", colorama.Fore.YELLOW, colorama.Back.RESET, colorama.Style.BRIGHT, 3
SUCCESS = "S", colorama.Fore.GREEN, colorama.Back.RESET, colorama.Style.BRIGHT, 4
INFO = "I", colorama.Fore.BLUE, colorama.Back.RESET, colorama.Style.NORMAL, 5
DEBUG = "D", colorama.Fore.WHITE, colorama.Back.RESET, colorama.Style.NORMAL, 6

LOG_LEVEL = DEBUG

def log_level(level):
    global LOG_LEVEL
    LOG_LEVEL = level

def init_log():
    colorama.init()
    print(colorama.Style.BRIGHT + 
          colorama.Back.GREEN + 
          colorama.Fore.BLACK + 
          "     >----- Interpreter starting -----<     " +
          colorama.Style.RESET_ALL)

def log(module, type, message):
    global LOG_LEVEL
    if(type[-1] > LOG_LEVEL[-1]):
        return

    style = "".join(type[1:-1])
    white = colorama.Fore.WHITE + colorama.Back.RESET + colorama.Style.NORMAL
    reset = colorama.Style.RESET_ALL
    
    print(style + "[" +
          white + module +
          style + "](" +
          white + type[0] +
          style + ") " + message +
          reset, end="", sep="")

def logln(module, type, message):
    log(module, type, message + '\n')