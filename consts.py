import json
import getpass
from utils import PathDir
import os

ROOT_PATH = PathDir(os.path.join(os.path.dirname(os.path.abspath(__file__))))

CONFIGS = json.load(open(os.path.join(ROOT_PATH.abs, 'config.json'), 'r'))

BASE_DIR = PathDir(
    CONFIGS["base-dir"].replace('$HOME', f'/home/{getpass.getuser()}'))
BASE_URL = PathDir(CONFIGS["base-url"])
TEMP_DIR = PathDir(CONFIGS["temp-dir"])

KINDLE_W_CONST = CONFIGS['width']
KINDLE_H_CONST = CONFIGS['height']

