import os


import xdg_base_dirs


APP_NAME = 'epaper-telegram'
DATA_DIR_PATH = os.path.join(xdg_base_dirs.xdg_data_home(), APP_NAME)
if not os.path.exists(DATA_DIR_PATH):
    os.makedirs(DATA_DIR_PATH)

ACCOUNTS_CREATED_FILE = 'accounts_created.ini'
path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
if not os.path.exists(path):
    open(path, 'w').close()

CORRESP_JID_FILE = 'correspondant_jid'
path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
if not os.path.exists(path):
    open(path, 'w').close()
