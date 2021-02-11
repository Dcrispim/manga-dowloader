import os
from pdfconverter import convertFolder, fit_images_by_folder, fix_images_by_folder
import cv2
import getpass
from time import sleep

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
try:
    os.mkdir(BASE_DIR)

except:
    pass


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
    os.system('clear')
    fullBar = ''.join([fullChar for i in range(0, lenFull+1)])
    emptyBar = ''.join([emptyChar for i in range(0, lenBar-lenFull+1)])
    return f"{msg}\n\n{fullBar}{emptyBar}"


def download_images(name, cap, dirName=None, title='', percent=None):
    pages_link = get_manga_images_link(name, cap, 100)

    try:
        if dirName == None:
            os.mkdir(getNameCap(name, cap))

    except:
        pass

    cmds = []
    for page in pages_link:

        cmd = 'clear'
        if percent:
            cmd += f" && {os.path.join(os.path.dirname(os.path.abspath(__file__)),'progressbarr.sh')} {int(percent*100)} '{title}'"
        else:
            cmd += f" && ./progressbarr.sh 0 '{title}'"
        cmd += f' && wget {page} -P {dirName or f"{getNameCap(name,cap)}"}'
        cmds.append(cmd)
    os.system('&&'.join(cmds))


def download_manga(name, end, start=1, dirname=None, especials=[], exclude=[]):

    def sortNumberString(key: str):
        return float(key.replace('-', '.').replace(',', '.'))

    caps = [str(cap) for cap in range(int(start or '1'), int(end)+1)]
    caps.extend([str(c) for c in especials])
    caps.sort(key=sortNumberString)
    manganame = f'{dirname or BASE_DIR}/{name}'
    try:
        if dirname == None:
            os.mkdir(f'{manganame}/jpgs')
    except:
        pass
    i = start
    for cap in caps:

        if cap not in exclude:

            dirnamecapname = getNameCap(name, cap, dirname)
            namecap = ' '.join([c.capitalize()
                                for c in dirnamecapname.split('/')[-1].split('-')])
            dirJPGcapname = os.path.join(
                manganame, 'jpgs', namecap.replace(' ', '_').lower())
            try:
                os.mkdir(os.path.join(manganame, 'jpgs'))
            except FileExistsError:
                pass
            except Exception as err:
                print(err)

            try:
                os.mkdir(dirJPGcapname)
            except FileExistsError:
                pass
            except Exception as err:
                print(err)
            download_images(name, cap, dirJPGcapname, namecap,
                            i/(len(caps)-len(exclude)))
            fix_images_by_folder(dirJPGcapname)
            fit_images_by_folder(dirJPGcapname)
            sleep(2)
            convertFolder(dirJPGcapname, manganame, namecap)
            print(dirJPGcapname, '\n')
        i += 1
    os.system('clear')
    print(f'finish {name}')


download_manga(mangaName, mangaEndPage, mangaStartPage,
               mangaDirName,  especials, exclude)
