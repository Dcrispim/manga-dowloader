from consts import BASE_DIR, BASE_URL, ROOT_PATH
import os
from utils import PathDir, createFolderIfNotExists, getExtension
from pdfconverter import convertFolder, fit_images_by_folder, fix_images_by_folder, isDuplicate
import cv2
import getpass
from time import sleep
from datetime import datetime
import requests

args = os.sys.argv[1:]

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
        decimal = f'.{getExtension(cap)}'

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
        decimal = f'.{getExtension(cap)}'

    clearCap = str(cap).split(".")[0]
    nameCap = f'{name}-cap{clearCap:0>4}{decimal if float(decimal or str(0))>0 else ""}'
    dirname = PathDir(dirname or BASE_DIR)

    return dirname.join(name, nameCap)


def log_bar(value, min=0, max=100, lenBar=100, msg='', emptyChar='-', fullChar='='):
    try:
        lenFull = int((value/(max-min))*lenBar)
    except ZeroDivisionError:
        lenFull = int((value/(max))*lenBar)
    # os.system('clear')
    fullBar = ''.join([fullChar for i in range(0, lenFull+1)])
    emptyBar = ''.join([emptyChar for i in range(0, lenBar-lenFull+1)])
    return f"{msg}\n\n{fullBar}{emptyBar}"


def download_image(pic_url, name):
    with open(str(name), 'wb') as handle:
        response = requests.get(str(pic_url), stream=True)

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

    for page in pages_link:
        page_dir = PathDir(page)
        os.system('clear')
        if percent:
            os.system(
                f"{ROOT_PATH.join('progressbarr.sh')} {int(percent*100)} '{title}'")
        else:
            os.system(f"{ROOT_PATH.join('progressbarr.sh')} 0 '{title}'")

        nameImage = PathDir((dirName or f"{getNameCap(name,cap)}")).join(
            page_dir.basename)
        print(page)
        try:
            download_image(page, nameImage)
            isdub = isDuplicate(
                nameImage, (dirName or f"{getNameCap(name,cap)}"))
            if isdub:
                print(isdub)
                break
        except Exception as err:

            print(err, 'line 138')
            break
        finally:
            if nameImage.size < 10:
                print(nameImage)
                os.remove(nameImage.abs)


def download_manga(name, end, start=1, dirname=None, especials=[], exclude=[]):

    def sortNumberString(key: str):
        return float(key.replace('-', '.').replace(',', '.'))

    caps = [str(cap) for cap in range(int(start or '1'), int(end)+1)]
    caps.extend([str(c) for c in especials])
    caps.sort(key=sortNumberString)

    dir_name = PathDir(dirname or BASE_DIR)
    manganame = dir_name.join(name)

    createFolderIfNotExists(manganame)
    createFolderIfNotExists(manganame.join('jpgs'))

    i = 1
    for cap in caps:

        if cap not in exclude:

            dirnamecapname = getNameCap(name, cap, dir_name)
            namecap = ' '.join([c.capitalize()
                                for c in dirnamecapname.basename.split('-')])
            dirJPGcapname = PathDir(
                manganame, 'jpgs', namecap.replace(' ', '_').lower())

            createFolderIfNotExists(dirJPGcapname)

            download_images(name, cap, dirJPGcapname.abs, namecap,i/(len(caps)-len(exclude)))
            fix_images_by_folder(dirJPGcapname)
            fit_images_by_folder(dirJPGcapname)
            convertFolder(dirJPGcapname, manganame, namecap)
            print(dirJPGcapname, '\n')
        i += 1
    # os.system('clear')
    print(f'finish {name}')


with open('./log', 'a+') as log:
    log.write(f'{datetime.now()}: START {mangaName} cap-{mangaStartPage} to cap-{mangaStartPage} and {especials} EXCLUDING {exclude}\n')


download_manga(mangaName, mangaEndPage, mangaStartPage,
               mangaDirName,  especials, exclude)


with open('./log', 'a+') as log:
    log.write(f'{datetime.now()} END {mangaName}\n')
