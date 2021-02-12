import os
import cv2

import numpy as np

KINDLE_W_CONST = 1072
KINDLE_H_CONST = 1448


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def fit_image(path: str):
    img = cv2.imread(os.path.join(path))
    try:
        ratio = KINDLE_W_CONST/img.shape[1]
        width = int(KINDLE_W_CONST*ratio)
        height = int(KINDLE_H_CONST*ratio)
        dim = (width, height)
        img_fit = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, img_fit)
    except Exception as err:
        print('FIT IMAGE ERROR: ', path, '\n', err)
        pass


def fix_image(path):
    img = cv2.imread(os.path.join(path))

    try:
        dimentions = img.shape

        if(dimentions[0] < dimentions[1]):
            img_rotate_90_clockwise = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(path, img_rotate_90_clockwise)
    except Exception as err:

        print('FIX IMAGE ERROR: ', path, '\n', err)
        return img


def fix_images_by_folder(folder):
    img_paths = os.listdir(folder)
    for imgPath in img_paths:
        if os.path.isfile(os.path.join(folder, imgPath)):
            try:
                fix_image(os.path.join(folder, imgPath))
            except Exception as err:
                print('FIX ALL IMAGEs ERROR: ', os.path.join(
                    folder, imgPath), '\n', err)

def fit_images_by_folder(folder):
    img_paths = os.listdir(folder)
    for imgPath in img_paths:
        if os.path.isfile(os.path.join(folder, imgPath)):
            try:
                fit_image(os.path.join(folder, imgPath))
            except Exception as err:
                print('FIT ALL IMAGEs ERROR: ', os.path.join(
                    folder, imgPath), '\n', err)



def convertFolder(folder: str, manganame=None, namecap=None):
    os.system(
        f'''echo "making PDF of cap {namecap or folder.split('/')[-1]}"''')
    manga_name = f"{manganame or folder.split('/')[-2]}"
    name_cap = f"{namecap or folder.split('/')[-1]}.pdf"
    root = os.path.join(*folder.split('/')[:-2])
    
    if folder[0] =='/':
        root = '/'+root

    convert_cmd = f'''convert {folder}/*.jpg "{os.path.join(root,manga_name,name_cap)}"'''
    os.system(convert_cmd)

    print(f'''create file {namecap or folder.split('/')[-1] }''')


def isDuplicate(imgPath:str, folder:str, trashhold=5, limit=7):
    img1 = cv2.imread(imgPath)
    try:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    except:
        pass
    imgs = os.listdir(folder)
    imgs.sort()
    for imgName in imgs[:limit] :
        if imgPath!=os.path.join(folder,imgName):
            try:
                img2 = cv2.imread(os.path.join(folder, imgName))
                try:
                    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                except:
                    pass
                err = mse(img1, img2)
                if err<trashhold:
                    
                    return True
            except:
                pass


if __name__ == "__main__":
    img1 = './52.jpg'
    imgDir = '/home/intelie/Documents/mangas/ajin/jpgs/ajin_cap0001/'
    args = os.sys.argv[1:]
    convertFolder(*args)
