import os
from pathdir import PathDir
from utils import cap_words
from pdfconverter import acessFolder, convertFolder


if __name__ == "__main__":
    args = os.sys.argv[1:]
    folder = PathDir(args[1])
    manganame = folder.basename.split('_')[0].strip('-').lower()
    cap = cap_words(f"{manganame} cap{folder.basename.split('_')[1]:0>4}".replace('-',' '))
    convertFolder(folder, folder.parent.parent, cap)

