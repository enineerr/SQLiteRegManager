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


@staticmethod
def padAllItems(l: list[list[str | int]]) -> list[list[str]]:
    # Create length list for comparison
    length = []
    for i in range(len(l[0])):
        length.append(0)

    # Find longest data for each field
    for i in range(len(l)):
        # Make each ID a str for manipulation
        l[i][0] = str(l[i][0])
        # Get each record individually
        for j in range(len(l[i])):
            # if the length of the value is longer, set it as max for field
            if (len(l[i][j]) > length[j]):
                length[j] = len(l[i][j])

    # Pad data
    for i in range(len(l)):
        for j in range(len(l[i])):
            # if is ID field, add left side vbar
            if (j == 0):
                l[i][j] = "|" + l[i][j].rjust(length[j])
            # always add right side vbar
            l[i][j] = l[i][j].ljust(length[j]) + "|"

    return l


@staticmethod
def printObj(recs: list[list[int | str]], msg: list[str]) -> None:
    # Add header
    recs.insert(0, msg)
    recs = padAllItems(recs)

    out = ""
    for i in recs:
        for j in i:
            out += j
        out += "\n"

    clear()
    # Print whole table
    print(out)
