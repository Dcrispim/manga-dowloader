import os

from numpy import number


class PathDir:
    def __init__(self, folder):
        self.folder = folder
    
    @property
    def parent(self):
        print('inner---', self)
        return PathDir(os.path.dirname(self.folder))
    
    @property
    def basename(self):
        return os.path.basename(self.folder)

    def __repr__(self):
        return self.folder

    def __str__(self):
        return self.__repr__()

    def abs(self):
        return os.path.dirname(self.folder)


class PathFile(PathDir):
    def __init__(self, folder):
        super().__init__(folder)
    
    @property
    def ext(self):
        return str(self.basename).split('.')[-1]
    @property
    def name(self):
        return str(self.basename).split('.')[0]

def createFolderIfNotExists(folder_path, *folders):
    try:
        os.mkdir(os.path.join(folder_path, *folders))
    except FileExistsError:
        pass
    except Exception as err:
        print(err)


def getExtension(file: str or number):
    return str(file).split('.')[-1]


def getParentDir(folder: str):
    return PathDir(folder)


