# coding=utf-8
"""
    everblog
    ~~~~~~~~
    Everblog is named after Evernote, you can publish your Evernote notes to Everblog as blog entries.
"""
from flask import Flask
from quick_orm.core import Database
from toolkit_library.encryption import Encryption


app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SECRET_KEY = Encryption.generate_random_string(),

    CONNECTION_STRING = 'sqlite:///everblog.db',
)

db = Database(app.config['CONNECTION_STRING'])


import everblog.blueprints
