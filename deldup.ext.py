from progressbar import progress
from manga import download_manga
from pdfconverter import convertFolder, fit_images_by_folder, isDuplicate
from consts import BASE_DIR
from pathdir import PathDir
from decorators import extension
import os


def parseCap(capnumber: str):
    if len(capnumber.split('_')) == 1:
        if len(capnumber.split('.')) == 2:
            return float(capnumber)
        else:
            return int(capnumber)

    elif len(capnumber.split('_')) == 2:

        _cap = capnumber.split('_')
        return f"{int(_cap[0])}-{_cap[1]}"


@extension
def removeDups(*args):
    folder = PathDir(BASE_DIR, str(args[0]).replace(' ', '-').lower(), 'jpgs')
    if len(args[1]) == 0:
        caps = [PathDir(folder, cp)
                for cp in folder.listdir if cp.isdir and len(cp.listdir) > 4]
    else:
        caps = [PathDir(folder, f'{folder.parent.basename}_cap{cp:0>4}')
                for cp in args[1]
                if PathDir(folder, f'{folder.parent.basename}_cap{cp:0>4}').isdir
                and len(PathDir(folder, f'{folder.parent.basename}_cap{cp:0>4}').listdir) > 4]

    print(caps)
    caps.sort()
    j = 0
    for cap in caps:
        change = False
        cap_imgs = cap.listdir
        cap_imgs.sort()
        i = 0
        for img in cap_imgs:
            os.system('clear')
            print(f'Checking {folder.parent.basename} cap {cap.basename}')
            progress((j/(len(caps)-1)), cap.basename)
            progress(i/(len(cap_imgs)-1), img.basename)
            isdub = isDuplicate(img.abs, cap.abs, limit=len(cap_imgs))
            if(isdub):
                print(f'Removing {img.basename}')
                change = True
                img.tryremove()
            i += 1
        if change:
            print(f'Converting {cap.basename}')
            convertFolder(cap.abs, folder.parent.basename, cap.basename)
        print('End checking')
        j += 1


if __name__ == "__main__":
    removeDups()
