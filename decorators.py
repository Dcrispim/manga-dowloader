import os
from pathdir import PathDir

def extension(ext: tuple):
    def __inter():
        args = os.sys.argv[1:]
        name = PathDir(args[1])
        ext(name, args[2:])
    return __inter
   