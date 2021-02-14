import os
from pathdir import PathDir

def extension(ext: tuple):
    args = os.sys.argv[1:]
    name = PathDir(args[1])
    return ext(name, args[2:])
   