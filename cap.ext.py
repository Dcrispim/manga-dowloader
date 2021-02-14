from consts import BASE_DIR
import os
from pathdir import PathDir
from utils import cap_words
from pdfconverter import acessFolder, convertFolder


if __name__ == "__main__":
    args = os.sys.argv[1:]
    name = PathDir(args[1].replace(' ','-').lower())
    manganame = name.basename.split('_')[0].strip('-').lower()
    caps = [PathDir(f'{name}_cap{cp:0>4}') for cp in args[2:]]
    for cap in caps:
        folder = PathDir(BASE_DIR,name,'jpgs',cap)
        convertFolder(folder, name, cap_words(cap.abs.replace('_', ' ')))

