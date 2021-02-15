from pathdir import PathDir
from decorators import extension
from utils import cap_words
from pdfconverter import acessFolder, convertFolder

@extension
def convertMain(*args):
    folder = PathDir(args[1].replace(' ','-').lower())
    manganame = folder.basename.split('_')[0].strip('-').lower()
    cap = cap_words(f"{manganame} cap{folder.basename.split('_')[1]:0>4}".replace('-',' '))
    convertFolder(folder, folder.parent.parent, cap)
    
if __name__ == "__main__":
   convertMain
