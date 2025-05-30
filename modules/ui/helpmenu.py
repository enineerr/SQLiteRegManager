from modules.ui.tui.terminal import maxLineLength


class helpMenu:
    def __init__(self):
        msg = {
            "-h --help": "Print this message",
            "-d --dbpath <path>": "Set path to the data dir relative to CWD"
        }
        # Get max length of cmdflag side of help menu
        maxLengthKey = maxLineLength(list(msg.keys())) + 2

        # Create a list of combined keys and values for calculation
        dictCombined = [k + v for k, v in msg.items()]
        # Get max length
        maxLengthLine = maxLineLength(dictCombined) + 4

        print("-" * maxLengthLine)
        for k, v in msg.items():
            # Add a basic separator
            k += ": "
            print(k.ljust(maxLengthKey) + v)

            print("-" * maxLengthLine)
