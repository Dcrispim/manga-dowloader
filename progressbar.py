from consts import ROOT_PATH
import os


def progress(percent, title):
    os.system(
        f"{ROOT_PATH.join('progressbarr.sh')} {int(percent*100)} '{title}'")

if __name__ == '__main__':
    progress(os.sys.argv[2],os.sys.argv[3])