import os


def createFolderIfNotExists(folder_path, *folders):
    try:
        os.mkdir(os.path.join(folder_path, *folders))
    except FileExistsError:
        pass
    except Exception as err:
        print(err)
