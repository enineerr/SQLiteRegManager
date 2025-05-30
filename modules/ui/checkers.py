# File full of basic checkers, sorting algorithms and filtering algorithms


@staticmethod
def checkName(inp: str) -> bool:
    for i in inp:
        match i:
            # allow dashes, spaces, and periods
            case "-" | " " | ".": pass
            case _:
                # Make sure everything else is a letter
                if (i.isalpha is not True):
                    # otherwise return false
                    return False

    return True


@staticmethod
def checkEmail(inp: str) -> bool:
    # if blank, allow to continue
    if (inp == ""):
        return True

    hasAt = False
    hasDot = False
    for i in inp:
        match i:
            case "@": hasAt = True
            # I know emails don't strictly have to have a TLD,
            # but ones without a TLD shouldn't be accepted anyway.
            case ".": hasDot = True

    return (hasAt and hasDot)


@staticmethod
def checkYN(inp: str) -> bool:
    match inp.lower()[:1]:
        case "y" | "n": return True
        case _: return False


@staticmethod
def checkINT(inp: str) -> bool:
    if (inp.isnumeric()):
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


# Finds the first instance in a list of lists with IDs and returns it
# otherwise returns a blank equal structure
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


# Same thing as above, but finds all instances of an ID,
# and allows setting where to look for ID
@staticmethod
def findAllIDs(
    l: list[list[int | str]],  # Input list of lists
    ID: int,  # ID to find
    index: int = 0  # which part of the list inside list to look for ID
) -> list[list[str | int | None]]:
    # Create empty list
    out = []
    # Iterate lvl1 list for ID at provided index
    for i in l:
        if (i[index] == ID):
            # Add whole list if ID is found
            out.append(i)

    # In case ID wasn't found
    if (out == []):
        out = []
        for i in range(len(l[0])):
            # Fill with equal number of blank outputs
            out.append("")
        # Place out into a list to mimic list[list[]]
        out = [out]

    return out
