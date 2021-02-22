from manga import download_manga
from numpy import number
from consts import BASE_DIR
from sys import path
from pathdir import PathDir
from decorators import extension


def parseCap(capnumber: str):
    if len(capnumber.split('_')) == 1:
        if len(capnumber.split('.')) == 2:
            return float(capnumber)
        else:
            return int(capnumber)

        
    elif len(capnumber.split('_')) == 2:
        
        _cap = capnumber.split('_')
        return f"{int(_cap[0])}-{_cap[1]}"


@extension
def convertEmptys(*args):
    folder = PathDir(BASE_DIR, str(args[0]).replace(' ', '-').lower(), 'jpgs')
    empty_caps = [PathDir(folder, cp)
                  for cp in folder.listdir if cp.isdir and len(cp.listdir) == 0]
    empty_caps.sort()
    download_manga(folder.parent.basename, None, 1, BASE_DIR, [
                   parseCap(n.basename.split('_cap')[-1]) for n in empty_caps])


if __name__ == "__main__":
    convertEmptys()
