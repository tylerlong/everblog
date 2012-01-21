# coding=utf-8
"""
    everblog.blueprints.static
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Static pages for the site
"""
from flask import Blueprint, render_template, abort, redirect, request, url_for, make_response
from sqlalchemy import func
from everblog import db
from everblog.models import Page
from everblog.blueprints import admin_required
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib


blueprint = Blueprint('page', __name__)


@blueprint.route('/<regex("(?:[a-z0-9]{3,16}|[\u4e00-\u9fa5]{2,8})"):title>/', methods = ['GET', ])
def read(title):
    """show a page"""
    page = db.session.query(Page).filter(func.lower(Page.title) == title.lower()).first()
    if not page:
        abort(404)
    etag = '"{0}"'.format(hashlib.sha256(str(page.updated)).hexdigest())
    if request.headers.get('If-None-Match', '') == etag:
        return '', 304
    last_modified = format_date_time(mktime(page.updated.timetuple()))
    if request.headers.get('If-Modified-Since', '') == last_modified:
        return '', 304    

    response = make_response(render_template('page/read.html', page = page))
    response.headers['ETag'] = etag
    response.headers['Last-Modified'] = last_modified
    return response


@blueprint.route('/p/create/', methods = ['POST', ])
@admin_required
def create():
    """create a page"""
    page = db.session.query(Page).filter_by(evernote_url = request.form['evernote_url']).first()
    if not page:
        page = Page(evernote_url = request.form['evernote_url'], order = request.form['order'])
        page.synchronize()
        db.session.add_then_commit(page)
    return redirect(url_for('admin.index'))
