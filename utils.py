import os
from pathdir import PathDir

from numpy import number


def createFolderIfNotExists(folder_path, *folders):
    try:
        os.mkdir(os.path.join(str(folder_path), *[str(f) for f in folders]))
    except FileExistsError:
        pass
    except Exception as err:
        print(err.__traceback__)


def getExtension(file: str or number):
    return str(file).split('.')[-1]


def getParentDir(folder: str):
    return PathDir(folder)

def cap_words(name: str):
    items = []
    for item in name.split():
        item = item.capitalize()
        items.append(item)
    return ' '.join(items)
