import os


def checkPath(pathFromRoot: str):
    result = False
    path = f"{os.getcwd()}/{pathFromRoot}"
    if os.path.exists(path):
        result = True
    return result


def deleteAllInSubdir(fileType: str, subdirPath: str = ""):
    # As it stands, this will only ever delete items in the named subfolder where this script runs.
    # Altering this function could cause it to delete the entire contents of other folders where you wouldn't want it to.
    # Alter this at your own risk.
    if subdirPath != "":
        deletePath = f"{os.getcwd()}/{subdirPath}"
        if os.path.exists(deletePath):
            for f in os.listdir(deletePath):
                if f.endswith(fileType):
                    os.remove(os.path.join(deletePath, f))
