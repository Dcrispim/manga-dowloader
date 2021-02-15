import os


class PathDir:
    def __init__(self, *folder):
        self.folder = os.path.join(*[str(p) for p in folder])

    @property
    def parent(self):
        return PathDir(os.path.dirname(self.folder))

    @property
    def basename(self):
        return os.path.basename(self.folder)

    @property
    def size(self):
        try:
            return int(os.path.getsize(self.abs))
        except:
            return 0

    @property
    def isfile(self):
        return os.path.isfile(self.abs)

    @property
    def isdir(self):
        return os.path.isdir(self.abs)

    @property
    def listdir(self):
        if self.isdir:

            return [PathDir(self.folder, f) if PathDir(self.folder, f).isdir else PathFile(self.folder,f) for f in os.listdir(self.abs)]
        else:
            return []

    def filter(self, child):
        return [f for f in self.listdir if f.basename == str(child)]

    def open(self, child):
        return self.filter(child)[0]

    def join(self, *folders):
        return PathDir(os.path.join(self.__str__(), *[str(p) for p in folders]))

    def tryremove(self):
        try:
            os.remove(self.abs)
        except Exception as err:
            print(f'Can not REMOVE {self.abs}: {err}')

    def __repr__(self):
        return self.__abs__()

    def __str__(self):
        return self.__repr__()


    @property
    def abs(self):
        return self.__abs__()

    def __abs__(self):
        return str(self.folder)

    def __ne__(self, b):
        return self.abs != PathDir(b).abs

    def __eq__(self, b):
        return self.abs == PathDir(b).abs
    
    def __lt__(self, b):
        return self.abs < PathDir(b).abs


class PathFile(PathDir):
    def __init__(self, *folder):
        super().__init__(*folder)

    @property
    def ext(self):
        return str(self.basename).split('.')[-1]

    @property
    def name(self):
        return str(self.basename).split('.')[0]

    def addExt(self, ext):
        self.folder = f"{self.folder}.{ext}"
        return self
