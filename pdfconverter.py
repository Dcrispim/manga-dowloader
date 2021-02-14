from consts import BASE_DIR, KINDLE_H_CONST, KINDLE_W_CONST, TEMP_DIR
import os
from utils import createFolderIfNotExists
from pathdir import PathDir, PathFile
import cv2
import zipfile
import numpy as np


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def fit_image(path: PathFile):
    img = cv2.imread(str(path))

    try:

        ratio = KINDLE_W_CONST/img.shape[1]

        width = int(KINDLE_W_CONST*ratio)
        height = int(KINDLE_H_CONST*ratio)
        dim = (width, height)
        img_fit = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(path.abs, img_fit)
    except Exception as err:

        print('FIT IMAGE ERROR: ', path, '\n', err)
        pass


def fix_image(path: PathFile):
    img = cv2.imread(str(path))

    try:
        dimentions = img.shape

        if(dimentions[0] < dimentions[1]):
            img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(path.abs, img_rotate_90_clockwise)
    except Exception as err:

        print('FIX IMAGE ERROR: ', path, '\n', err)
        return img


def fix_images_by_folder(folder):
    img_paths = PathDir(folder).listdir
    for imgFile in img_paths:
        if imgFile.isfile:
            try:
                fix_image(imgFile)
            except Exception as err:
                print('FIX ALL IMAGEs ERROR: ', imgFile.name, '\n', err)


def fit_images_by_folder(folder):
    img_paths = PathDir(folder).listdir

    for imgFile in img_paths:

        if imgFile.isfile:

            try:

                fit_image(imgFile)
            except Exception as err:
                print('FIT ALL IMAGEs ERROR: ', imgFile, '\n', err)


def convertFolder(folder: str, manganame=None, namecap=None):

    folder_dir = PathDir(folder)
    os.system(
        f'''echo "making PDF of cap {namecap or folder_dir.basename}"''')
    manga_name = PathDir(manganame or folder_dir.parent.parent.basename)
    name_cap = PathFile(namecap or folder_dir.parent.basename).addExt('pdf')
    root = folder_dir.parent.parent.parent
    createFolderIfNotExists(root.join(manga_name))
    convert_cmd = f'''convert {folder}/*.jpg "{root.join(manga_name,name_cap)}"'''
    os.system(convert_cmd)

    print(f'''create file {root.join(manga_name,name_cap)}''')


def isDuplicate(imgPath: str, folder: str, trashhold=5, limit=7):
    img1 = cv2.imread(str(imgPath))
    try:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    except:
        pass
    imgs = os.listdir(str(folder))
    imgs.sort()
    for imgName in imgs[:limit]:
        if imgPath != PathFile(folder, imgName):
            try:
                img2 = cv2.imread(PathFile(folder, imgName).abs)
                try:
                    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                except:
                    pass
                err = mse(img1, img2)
                if err < trashhold:

                    return True
            except:
                pass


def acessFolder(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip:
        file = PathFile(file_path)
        zip.extractall(BASE_DIR.join('.temp', file.name).abs)

        return BASE_DIR.join('.temp', file.name)


if __name__ == "__main__":
    fit_images_by_folder(
        '/home/intelie/Documents/mangas/ajin/jpgs/ajin_cap0001')
