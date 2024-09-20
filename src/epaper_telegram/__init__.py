import os


import xdg_base_dirs


APP_NAME = 'epaper-telegram'
DATA_DIR_PATH = os.path.join(xdg_base_dirs.xdg_data_home(), APP_NAME)
if not os.path.exists(DATA_DIR_PATH):
    os.makedirs(DATA_DIR_PATH)
