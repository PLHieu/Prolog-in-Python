def isUpper(string):
    if (string[0].isupper()):
        return True
    return False


def isLower(string):
    if (string[0].islower()):
        return True
    return False

def haveElementUppercase(l):
    for str in l:
        if isUpper(str):
            True
    return False