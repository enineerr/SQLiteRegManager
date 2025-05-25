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

        inp = input(">>> ")

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
    accepted = False
    while (accepted is False):
        print("Is this correct? (y/n)")
        accepted = validateInput(checkYN)

    return accepted.lower()[:1]  # type: ignore


@staticmethod
def editHumanMenu() -> int:
    msg = {
        "(1)": "Edit First Name",
        "(2)": "Edit Middle Name",
        "(3)": "Edit Last Name",
        "(4)": "Edit Chosen Name",
        "(5)": "Edit Email",
        "(q)": "Go Back"
    }

    while True:
        clear()
        printMenu(msg)

        inp = input(">>> ")

        # Process input
        match inp.lower():
            case "1" | "2" | "3" | "4" | "5":
                return int(inp)
            case "q": return 0
            # If invalid input, restart loop, skipping exit
            case _: continue


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
