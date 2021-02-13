import os
from utils import cap_words
from pdfconverter import acessFolder, convertFolder


if __name__ == "__main__":
    args = os.sys.argv[1:]
    ZIP = acessFolder(args[1])
    manganame = ZIP.basename.split('_-_')[0].strip('-').lower()
    cap = cap_words(f"{manganame} cap{ZIP.basename.split('_-_')[1]:0>4}".replace('-',' '))
    convertFolder(ZIP.open('content'), ZIP.parent.parent.join(manganame), cap)

