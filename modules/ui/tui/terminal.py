@staticmethod
def clear():
    # I dont like this
    # the day python implements a terminal clear, the world will be whole
    print("\n"*100)


@staticmethod
def maxLineLength(calcLines: list[str]) -> int:
    maxLength = 0
    for i in calcLines:
        if len(i) > maxLength:
            maxLength = len(i)
    return maxLength


@staticmethod
def printMenu(msg: dict[str, str]) -> None:
    for k, v in msg.items():
        # Add a basic separator
        k += ":"
        print(k, v)
