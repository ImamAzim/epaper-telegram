import os


import xdg


APP_NAME = 'epaper-telegram'
DATA_DIR_PATH = os.path.join(xdg.xdg_data_home(), APP_NAME)
if not os.path.exists(DATA_DIR_PATH):
    os.makedirs(DATA_DIR_PATH)

STATE_DIR_PATH = os.path.join(xdg.xdg_state_home(), APP_NAME)
if not os.path.exists(STATE_DIR_PATH):
    os.makedirs(STATE_DIR_PATH)

ACCOUNTS_CREATED_FILE = os.path.join(DATA_DIR_PATH, 'accounts_created.ini')
path = ACCOUNTS_CREATED_FILE
if not os.path.exists(path):
    open(path, 'w').close()

LOGFILE = os.path.join(STATE_DIR_PATH, 'epaper-telegram.log')
path = LOGFILE
if not os.path.exists(path):
    open(path, 'w').close()

DAEMON_ENTRY_POINT = '_epaper-telegramd'  # Must be present in pyproject.toml!
