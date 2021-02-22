from consts import BASE_DIR
from decorators import extension
from pathdir import PathDir
from utils import cap_words
from pdfconverter import acessFolder, convertFolder

@extension
def convertCap(*args):
    print(args)
    name = PathDir(str(args[0]).replace(' ','-').lower())
    caps = [PathDir(f'{name}_cap{cp:0>4}') for cp in args[1]]
    for cap in caps:
        folder = PathDir(BASE_DIR,name,'jpgs',cap)
        convertFolder(folder, name, cap_words(cap.abs.replace('_', ' ')))

if __name__ == "__main__":
   convertCap()

