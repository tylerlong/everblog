# coding=utf-8
"""
    everblog.blueprints.static
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Static pages for the site
"""
import os
from everblog import app
from flask import Blueprint, render_template, abort


blueprint = Blueprint('static', __name__)


@blueprint.route('/<regex("[a-z]{2,16}"):page>/', methods = ['GET', ])
def read(page):
    if not os.path.exists(os.path.join(app.root_path,'templates/static/{0}.html'.format(page))):
        abort(404)
    return render_template('static/{0}.html'.format(page))
