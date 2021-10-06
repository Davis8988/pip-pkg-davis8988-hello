# Color printings using colorama pkg

from colorama import Fore, Back, Style, init

# Consider adding some info printings: print("Colorama init")
# Can also use: init()
init(autoreset=True)

def coloredprint(msg='', foreground_color=None, **kwargs):
	background_color = kwargs.get("background_color", None)
	if background_color:
		print(getattr(Back, background_color) + getattr(Fore, foreground_color) + f"{msg}")
	else:
		print(getattr(Fore, foreground_color) + f"{msg}")


def print_msg(msg):
	print(msg)
