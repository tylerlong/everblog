# coding=utf-8
"""
    wsgi
    ~~~~
    To be invoked by a web server which supports wsgi
"""
VIRTUALENV_PATH = '/srv/envs/prod/'
PROJECT_PATH = '/srv/www/everblog/'

import os
# Activate virtualenv
activate_this = os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
execfile(activate_this, dict(__file__ = activate_this))

import sys
# add project folder to sys.path
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

# mod_wsgi requires a variable named application
from everblog import app as application
