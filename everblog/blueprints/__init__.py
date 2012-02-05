# coding=utf-8
"""
    everblog.blueprints
    ~~~~~~~~~~~~~~~~~~~
    blueprints for the whole application
"""
import sys, datetime
from functools import wraps
from flask import g, redirect, session, url_for
from toolkit_library.inspector import PackageInspector
from everblog import app, db
from everblog.models import Page


def admin_required(f):
    """function decorator, force user to login as administrator."""
    @wraps(f)
    def decorated(*args, **kwds):
        if not 'admin' in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwds)            
    return decorated


def before_request():
    """called before every request"""
    g.pages = db.session.query(Page).order_by(Page.order)
    g.contacts = app.config['CONTACT_METHODS']
    g.blog_owner = app.config['BLOG_OWNER']
    g.time_zone = datetime.timedelta(hours = app.config['TIME_ZONE'])
    g.google_analytics_tracking_id = app.config['GOOGLE_ANALYTICS_TRACKING_ID']


def teardown_request(exception = None):
    """called after every request"""
    db.session.remove()


packageInspector = PackageInspector(sys.modules[__name__])
all_blueprints = packageInspector.get_all_modules()
for blueprint in all_blueprints:
    #import blueprint
    exec('from everblog.blueprints import {0}'.format(blueprint))
    #register before_request to every blueprint
    exec('{0}.blueprint.before_request(before_request)'.format(blueprint))
    #register teardown_request to every blueprint
    exec('{0}.blueprint.teardown_request(teardown_request)'.format(blueprint))
    #register blueprint to app
    exec('app.register_blueprint({0}.blueprint)'.format(blueprint)) 
