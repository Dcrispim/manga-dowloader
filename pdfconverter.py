import os
import cv2

KINDLE_W_CONST = 1072
KINDLE_H_CONST = 1448


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


if __name__ == "__main__":
    args = os.sys.argv[1:]
    convertFolder(*args)
