# coding=utf-8
"""
    everblog
    ~~~~~~~~
    Everblog is named after Evernote, you can publish your Evernote notes to Everblog as blog entries.
"""
__author__ = 'Tyler Long'
__version__ = '0.2.5'


from flask import Flask
from werkzeug.routing import BaseConverter
from quick_orm.core import Database
from toolkit_library.encryption import Encryption


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.update(
    DEBUG = True,
    SECRET_KEY = Encryption.generate_random_string(),

    CONNECTION_STRING = 'postgresql://tyler:123456@localhost/everblog',
    IMAGE_CACHE = 'everblog/everblog.dbm',

    ADMIN_USERNAME = 'admin',
    ADMIN_PASSWORD = 'password',
    BLOG_OWNER = 'Tyler Long',
    CONTACT_METHODS = [
        ('email', 'mailto:mituzhishi@gmail.com'),
        (u'微博', 'http://weibo.com/tylerlong'),
        ('github', 'https://github.com/tylerlong'),
        ('bitbucket', 'https://bitbucket.org/tylerlong'),
        ('stackoverflow', 'http://stackoverflow.com/users/862862/tyler-long'),
    ],

    DEFAULT_LANG = 'en',
    TIME_ZONE = +8,
    PAGE_SIZE = 8,

    #third party settings
    DISQUS_SHORTNAME = 'tylerlong',
    GOOGLE_ANALYTICS_TRACKING_ID = 'UA-28950403-1'
)

db = Database(app.config['CONNECTION_STRING'])

import everblog.blueprints
