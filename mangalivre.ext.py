from decorators import extension
from utils import cap_words
from pdfconverter import acessFolder, convertFolder

@extension
def convertZip(*args):
    ZIP = acessFolder(args[0])
    manganame = ZIP.basename.split('_-_')[0].strip('-').lower()
    cap = cap_words(f"{manganame} cap{ZIP.basename.split('_-_')[1]:0>4}".replace('-',' '))
    convertFolder(ZIP.open('content'), ZIP.parent.parent.join(manganame), cap)

if __name__ == "__main__":
    convertZip

