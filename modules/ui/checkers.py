@staticmethod
def checkName(inp: str) -> bool:
    for i in inp:
        if (i == "-"):
            pass
        # This elif dirties a match/case
        elif (i.isalpha() is not True):
            return False

    return True


@staticmethod
def checkEmail(inp: str) -> bool:
    # if blank, allow to continue
    if inp == "":
        return True

    hasAt = False
    hasDot = False
    for i in inp:
        if i == "@":
            hasAt = True
        elif i == ".":
            hasDot = True

    return (hasAt and hasDot)


@staticmethod
def checkYN(inp: str) -> bool:
    match inp.lower()[:1]:
        case "y" | "n": return True
        case _: return False


@staticmethod
def checkINT(inp: str) -> bool:
    if inp.isnumeric():
        return True
    return False


# Basic bubble sort, but modified to use the ID from a list of records
@staticmethod
def sortListsByID(l: list[list[int | str]]) -> list[list[int | str]]:
    check = True
    while check:
        check = False
        for i in range(len(l) - 1):
            if l[i][0] > l[i+1][0]:
                l[i][0] += l[i+1][0]
                l[i+1][0] = l[i][0] - l[i+1][0]
                l[i][0] -= l[i+1][0]
                check = True
    return l


@staticmethod
def findID(l: list[list[int | str]], ID: int) -> list[int | str | None]:
    for i in l:
        if (i[0] == ID):
            return i

    # In case ID wasn't found
    out = [None]
    # Skip first part, since that needs to be None for ID
    for i in range(1, len(l[0])):
        out.append("")
    # Return equal length of None
    return out
