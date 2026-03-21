import colorama

from typing import Tuple

"""
Plik zawiera funkcje do wyświetlania sformatowanych komunikatów do konsoli.

[<tag>](<type>) <message>

<tag> = krótki napis identyfikujący, z której części programu pochodzi wiadomość
<type> = jak ważne jest to co tam pisze
<message> = treść

Poziomy logowania to:
1. Fatal - błąd przez, który nie jest możliwa kontynuacja 
         -> kolor czerwony

2. Error - błąd, który uniemożliwia wykonanie czegoś, ale program może kontynuować
         -> kolor czerwony

3. Warning - ostrzeżenie
         -> kolor żółty/pomarańczowy

4. Success - pomyślne wykonanie operacji
         -> kolor zielony

5. Info - Informacja, np. rozpoczęcie wykonanywania operacji, przejście do następnego kroku
         -> kolor niebieski

6. Debug - Szczegółowe informacje, które są nikomu nie potrzebne jeśli wszystko jest ok
         -> kolor biały

Ukrycie wiadomości o wyższym poziome jest możliwe zmniejszając poziom logowania
poprzez przypisanie odpowiedniego poziomu wywołaniem funkcji:. 

log_level(SUCCESS) -> wyświetlane jest FALTA, ERROR, WARNING i SUCCESS

Inicjalizacja - przed pierwszym wyświetlonym komunikatem wywołaj:
init_log()

Wyświetlanie komunikatów:

log(module, type, message, end=True, only_msg=False)

module -> module tag: INIT, PLACE, ...
type -> message type: FATAL, INTO, ...
message -> the message
end -> if True there is no \n at the end
only_msg -> if True only the message is shown, without the module tag and type

Przykładowe użycie

log(INIT, INFO, "Przetwarzam...", end=False)
...
except ...:
    log(INIT, FATAL, "Coś się wysypało")
...
log(INIT, SUCCESS, "OK", only_msg=True)

co wyświetlone będzie jako:
[INIT ](I) Przetwarzam...OK
a w przypadku błędu:
[INIT ](I) Przetwarzam...
[INIT ](F) Coś się wysypało

"""
# Module tags, add more if needed, but make everything the same length
INIT =    "INIT " # Initialization
PLACE =   "PLACE" # Place divide/Place run
SC_ER =   "SC ER" # ScriptErrors
QNET =    "Q NET" # Quantum Network
OBS =     " OBS " # Observation
STATE =   "STATE" # Quantum state

# Types, do not add more, this is enough
# NOTHING is used only for disabling the entire logging
NOTHING = " ", colorama.Fore.RED, colorama.Back.RESET, colorama.Style.BRIGHT, 0  
FATAL = "F", colorama.Fore.RED, colorama.Back.RESET, colorama.Style.BRIGHT, 1
ERROR = "E", colorama.Fore.RED, colorama.Back.RESET, colorama.Style.BRIGHT, 2
WARNING = "W", colorama.Fore.YELLOW, colorama.Back.RESET, colorama.Style.BRIGHT, 3
SUCCESS = "S", colorama.Fore.GREEN, colorama.Back.RESET, colorama.Style.BRIGHT, 4
INFO = "I", colorama.Fore.BLUE, colorama.Back.RESET, colorama.Style.NORMAL, 5
DEBUG = "D", colorama.Fore.WHITE, colorama.Back.RESET, colorama.Style.NORMAL, 6

# Styles of each level
STYLE_NOTHING = colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
STYLE_FATAL = colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
STYLE_ERROR = colorama.Fore.RED + colorama.Back.RESET + colorama.Style.BRIGHT
STYLE_WARNING = colorama.Fore.YELLOW + colorama.Back.RESET + colorama.Style.BRIGHT
STYLE_SUCCESS = colorama.Fore.GREEN + colorama.Back.RESET + colorama.Style.BRIGHT
STYLE_INFO = colorama.Fore.BLUE + colorama.Back.RESET + colorama.Style.NORMAL
STYLE_DEBUG = colorama.Fore.WHITE + colorama.Back.RESET + colorama.Style.NORMAL
# + some more 
STYLE_DEBUG_CYAN = colorama.Fore.CYAN + colorama.Back.RESET + colorama.Style.NORMAL
STYLE_DEBUG_YELLOW = colorama.Fore.YELLOW + colorama.Back.RESET + colorama.Style.NORMAL
STYLE_DEBUG_MAGENTA = colorama.Fore.MAGENTA + colorama.Back.RESET + colorama.Style.NORMAL




# Default log level, show everything
LOG_LEVEL = DEBUG

def log_level(level: Tuple[str, str, str, str, int]) -> None:
    """
    Sets the debug level

    Parameters:
        level: one of: FATAL, ERROR, WARNING, SUCCESS, INFO, DEBUG
    """
    global LOG_LEVEL
    LOG_LEVEL = level

def init_log() -> None:
    """
    Initializes debugger and shows the startup message
    """
    colorama.init()
    if LOG_LEVEL != NOTHING:
        print(colorama.Style.BRIGHT + 
            colorama.Back.GREEN + 
            colorama.Fore.BLACK + 
            "     >----- Interpreter starting -----<     " +
            colorama.Style.RESET_ALL)

# This variable is for remembering if the last log ended with a newline or not
LOG_LAST_LINE_NO_END = False

def log(module: str, type: str, message: str, end: bool = True, only_msg: bool = False) -> None:
    """
    Log a message, see the comment at the top how to use this
    """

    def has_endline():
        """
        Returns True if this log will end with \n
        """
        nonlocal message
        nonlocal end

        return end or message[-1] == '\n'


    global LOG_LEVEL
    global LOG_LAST_LINE_NO_END

    # Stop here if current log level is too low
    if(type[-1] > LOG_LEVEL[-1]):
        return

    # Prepare current style, white style and reset commands
    style = "".join(type[1:-1])
    white = colorama.Fore.WHITE + colorama.Back.RESET + colorama.Style.NORMAL
    reset = colorama.Style.RESET_ALL

    # How will the line end
    end_type = "\n" if end else ""

    if only_msg:
        # Only message(with its style) will get displayed, no tag
        print(style + message, end=end_type, sep="")
        # Update the endline flag
        LOG_LAST_LINE_NO_END = not has_endline()
        return
    
    # Check the endline flag
    if LOG_LAST_LINE_NO_END:
        # Previous log did not end with a newline, add it now
        print()
        LOG_LAST_LINE_NO_END = False
    elif not has_endline():
        LOG_LAST_LINE_NO_END = True

    # Display the tags and message
    print(style + "[" +                # '[' in the color of the message
          white + module +             # White text for <tag>
          style + "](" +               # '](' in the color of the messsage
          white + type[0] +            # White text for <type>
          style + ") " + message +     # ') ' in the color of the message + the message itself
          reset, end=end_type, sep="") # reset the styling to default and add a newline if set
    
