"""Config compiler."""

import os

# Base config DIR.
BASE_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_FILE = os.path.join(BASE_CONFIG_DIR, 'base.py')
LOCAL_FILE = os.path.join(BASE_CONFIG_DIR, 'local.py')
PROD_FILE = os.path.join(BASE_CONFIG_DIR, 'production.py')

execfile(BASE_FILE)

if os.path.isfile(LOCAL_FILE) is True:
    execfile(LOCAL_FILE)
else:
    execfile(PROD_FILE)
