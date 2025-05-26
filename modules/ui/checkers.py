@staticmethod
def checkName(inp: str) -> bool:
    for i in inp:
        if i == " ":
            return False
        elif i == "-":
            pass
        elif i.isalpha() is not True:
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
