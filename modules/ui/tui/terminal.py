from copy import deepcopy


@staticmethod
def clear():
    # I don't like this
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


@staticmethod
def padAllItems(inL: list[list[str | int]]) -> list[list[str]]:
    l = deepcopy(inL)
    # Create length list for comparison
    length = []
    for i in range(len(l[0])):
        length.append(0)

    # Find longest data for each field
    for i in range(len(l)):
        # Get each record individually
        for j in range(len(l[i])):
            # if the length of the value is longer, set it as max for field
            if (len(str(l[i][j])) > length[j]):
                length[j] = len(str(l[i][j]))

    # Pad data
    for i in range(len(l)):
        for j in range(len(l[i])):
            # if an int, pad left, and add right vbar
            if (type(l[i][j]) is int):
                l[i][j] = str(l[i][j]).rjust(length[j]) + "|"
            # if not a number, pad right, and add right vbar
            else:
                l[i][j] = str(l[i][j]).ljust(length[j]) + "|"
            if (j == 0):
                l[i][j] = "|" + l[i][j]

    return l


@staticmethod
def printObj(recsIn: list[list[int | str]], msg: list[str]) -> None:
    # Add header
    recs = deepcopy(recsIn)
    recs.insert(0, msg)
    recs = padAllItems(recs)

    out = ""
    for i in recs:
        out += "".join(i)
        out += "\n"

    clear()
    # Print whole table
    print(out)
