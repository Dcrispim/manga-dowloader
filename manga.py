import os
from utils import createFolderIfNotExists
from pdfconverter import convertFolder, fit_images_by_folder, fix_images_by_folder, isDuplicate
import cv2
import getpass
from time import sleep
from datetime import datetime
import requests

args = os.sys.argv[1:]


BASE_URL = 'https://cdn.mangayabu.top/mangas'
BASE_DIR = f'/home/{getpass.getuser()}/Documents/mangas'
slime = 'tensei-shitara-slime-datta-ken'
mangaName = args[0]
mangaEndPage = args[1]
mangaStartPage = 1
mangaDirName = None
especials = []
exclude = []

global cleanCap
cleanCap = False
global status

status = ''



for arg in args:
    if '--start' in arg:
        mangaStartPage = int(arg.split('=')[-1])

    if '--mangaDirName' in arg:
        mangaDirName = arg.split('=')[-1]

    if '--especials' in arg:
        if arg.split('=')[-1][0:2] == '//':
            with open(arg.split('=')[-1][2:]) as especialfile:
                for cap in especialfile.readlines()[0].split('/'):
                    try:
                        especials.append(float(cap))
                    except:
                        especials.append(cap)
        else:
            for cap in arg.split('=')[-1].split('/'):
                try:
                    especials.append(float(cap))
                except:
                    especials.append(cap)

    if '--exclude' in arg:
        exclude = [float(cap) for cap in arg.split('=')[-1].split('/')]

    if '--cleancap' in arg:
        cleanCap = True

createFolderIfNotExists(BASE_DIR)
createFolderIfNotExists(BASE_DIR, '.temp')

def get_manga_images_link(name: str, cap: int, endPage: int, startPage=1):
    decimal = ''
    if len(str(cap).split('.')) == 2:
        decimal = f'.{str(cap).split(".")[-1]}'

    if cleanCap:
        request = [
            f'{BASE_URL}/{name}/capitulo-{str(cap).split(".")[0]}{decimal}/{page}.jpg' for page in range(startPage, endPage+1)]

    else:
        request = [
            f'{BASE_URL}/{name}/capitulo-{str(cap).split(".")[0]:0>2}{decimal}/{page:0>2}.jpg' for page in range(startPage, endPage+1)]
    return request


def getNameCap(name, cap, dirname=None):
    decimal = ''
    if len(str(cap).split('.')) == 2:
        decimal = f'.{str(cap).split(".")[-1]}'

    return f'{dirname or BASE_DIR}/{name}/{name}-cap{str(cap).split(".")[0]:0>4}{decimal}'


def log_bar(value, min=0, max=100, lenBar=100, msg='', emptyChar='-', fullChar='='):
    try:
        lenFull = int((value/(max-min))*lenBar)
    except ZeroDivisionError:
        lenFull = int((value/(max))*lenBar)
    #os.system('clear')
    fullBar = ''.join([fullChar for i in range(0, lenFull+1)])
    emptyBar = ''.join([emptyChar for i in range(0, lenBar-lenFull+1)])
    return f"{msg}\n\n{fullBar}{emptyBar}"

def download_image(pic_url, name):
    with open(name, 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)
            raise Exception(response.status_code, pic_url)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)



def download_images(name, cap, dirName=None, title='', percent=None):
    pages_link = get_manga_images_link(name, cap, 100)

    if dirName == None:
        createFolderIfNotExists(getNameCap(name, cap))

    cmds = []
    for page in pages_link:
        os.system('clear')
        if percent:
            os.system(
                f"{os.path.join(os.path.dirname(os.path.abspath(__file__)),'progressbarr.sh')} {int(percent*100)} '{title}'")
        else:
            os.system(f"./progressbarr.sh 0 '{title}'")
        
        nameImage = os.path.join((dirName or f"{getNameCap(name,cap)}"),f"{page.split('/')[-1]}")
        print(page)
        try:
            download_image(page, nameImage)
            isdub= isDuplicate(nameImage,(dirName or f"{getNameCap(name,cap)}"))
            if isdub:
                print(isdub)
                break
        except Exception as err:
            print(err)
            break
        finally:
            if int(os.path.getsize(nameImage))<10:
                print(nameImage)
                os.remove(nameImage)


def download_manga(name, end, start=1, dirname=None, especials=[], exclude=[]):

    def sortNumberString(key: str):
        return float(key.replace('-', '.').replace(',', '.'))

    caps = [str(cap) for cap in range(int(start or '1'), int(end)+1)]
    caps.extend([str(c) for c in especials])
    caps.sort(key=sortNumberString)
    manganame = os.path.join(dirname or BASE_DIR, name)

    createFolderIfNotExists(manganame)
    createFolderIfNotExists(os.path.join(manganame, 'jpgs'))

    i = 1
    for cap in caps:

        if cap not in exclude:

            dirnamecapname = getNameCap(name, cap, dirname)
            namecap = ' '.join([c.capitalize()
                                for c in dirnamecapname.split('/')[-1].split('-')])
            dirJPGcapname = os.path.join(
                manganame, 'jpgs', namecap.replace(' ', '_').lower())
            
            createFolderIfNotExists(dirJPGcapname)

            download_images(name, cap, dirJPGcapname, namecap,
                            i/(len(caps)-len(exclude)))
            fix_images_by_folder(dirJPGcapname)
            fit_images_by_folder(dirJPGcapname)
            convertFolder(dirJPGcapname, manganame, namecap)
            print(dirJPGcapname, '\n')
        i += 1
    #os.system('clear')
    print(f'finish {name}')

with open('./log','a+') as log:
    log.write(f'{datetime.now()}: START {mangaName} cap-{mangaStartPage} to cap-{mangaStartPage} and {especials} EXCLUDING {exclude}\n')


download_manga(mangaName, mangaEndPage, mangaStartPage,
              mangaDirName,  especials, exclude)


with open('./log','a+') as log:
    log.write(f'{datetime.now()} END {mangaName}\n')
