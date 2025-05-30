from modules.ui.tui.terminal import clear, printMenu
from modules.ui.checkers import checkYN


@staticmethod
def multiMenu(msg: dict[str, str]) -> str:
    while True:
        pmsg = {}
        for but, m in msg.items():
            pmsg.update({f"({but})": m})

        clear()
        # Printed message building
        printMenu(pmsg)

        inp = input(">>> ").lower()

        # Process input
        # if valid key, return it
        if (inp in msg.keys()):
            return inp
        # otherwise, continue loop


# Takes a function as an arg,
# then takes an input from user,
# and uses function to check if valid,
# if valid, returns input
# else, false
@staticmethod
def validateInput(func) -> bool | str:
    inp = input(">>> ")
    # If input is valid, hand it to caller
    if func(inp):
        return inp
    else:
        clear()
        print("Please re-enter, invalid character entered.")
        return False


@staticmethod
def yn() -> str:
    try:
        accepted = False
        while (accepted is False):
            print("Is this correct? (y/n)")
            accepted = validateInput(checkYN)

        return accepted.lower()[:1]  # type: ignore
    except KeyboardInterrupt:
        # When user requests to leave, just output empty string
        return ""


@staticmethod
def getInfo(inp: dict) -> list[str | None]:
    try:
        # Init list now
        out = []

        # msg -> message to print on each run
        # func -> checker func to run
        for msg, func in inp.items():
            clear()
            # check flag becomes output of the run during loop
            accepted = False
            while (accepted is False):
                print(msg)
                accepted = validateInput(func)
            out.append(accepted)

        return out
    except KeyboardInterrupt:
        return [None]
