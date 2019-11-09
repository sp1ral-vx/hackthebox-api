'''HackTheBox colorize module.'''
from colorama import Fore


def colorize(color: str, message: str) -> str:
    '''Colorize output.

    :param str color  : color name.
    :param str message: message string.
    :rtype: str
    '''

    color = color.lower()
    if color == 'red':
        color = Fore.RED
    elif color == 'lightred':
        color = Fore.LIGHTRED_EX
    elif color == 'green':
        color = Fore.GREEN
    elif color == 'yellow':
        color = Fore.YELLOW
    elif color == 'blue':
        color = Fore.BLUE
    elif color == 'magenta':
        color = Fore.MAGENTA
    elif color == 'cyan':
        color = Fore.CYAN
    elif color == 'white':
        color = Fore.WHITE
    else:
        color = ''
    return color + message + Fore.RESET
