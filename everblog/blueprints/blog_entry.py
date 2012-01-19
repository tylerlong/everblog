# coding=utf-8
"""
    everblog.blueprints.blog_entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Notes from evernote, Which will be converted to blog entries.
"""
from flask import Blueprint, render_template, abort, redirect, url_for, request, make_response
from everblog import db
from everblog.models import BlogEntry
from everblog.blueprints import admin_required
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib

DEFAULT_LANG = 'en'
PAGE_SIZE = 8

blueprint = Blueprint('blog_entry', __name__)

@blueprint.route('/<regex("[a-z]{2}"):lang>/page/<int:page>/', methods = ['GET', ])
def list_lang_page(lang, page):
    if not lang in ('en', 'cn',) or page < 1:
        abort(404)
    blog_entries = db.session.query(BlogEntry).filter_by(lang = lang)
    hasNext = True if blog_entries.count() > page * PAGE_SIZE else False
    items = blog_entries.order_by(BlogEntry.created.desc()).slice(page * PAGE_SIZE - PAGE_SIZE, page * PAGE_SIZE)
    if items.count() < 1:
        abort(404)
    return render_template('blog_entry/list.html', lang = lang, page = page, items = items, hasNext = hasNext)

@blueprint.route('/<regex("[a-z]{2}"):lang>/', methods = ['GET', ])
def list_lang(lang):
    return list_lang_page(lang, 1)
@blueprint.route('/page/<int:page>/', methods = ['GET', ])
def list_page(page):
    return list_lang_page(DEFAULT_LANG, page)
@blueprint.route('/', methods = ['GET', ])
def list():
    return list_lang(DEFAULT_LANG)


@blueprint.route('/<int:id>/', methods = ['GET', ])
def read(id):
    blog_entry = db.session.query(BlogEntry).get(id)
    if not blog_entry:
        abort(404)
    etag = '"{0}"'.format(hashlib.sha256(str(blog_entry.updated)).hexdigest())
    if request.headers.get('If-None-Match', '') == etag:
        return '', 304
    last_modified = format_date_time(mktime(blog_entry.updated.timetuple()))
    if request.headers.get('If-Modified-Since', '') == last_modified:
        return '', 304    
    response = make_response(render_template('blog_entry/read.html', blog_entry = blog_entry))
    response.headers['ETag'] = etag
    response.headers['Last-Modified'] = last_modified
    return response


@blueprint.route('/create/', methods = ['POST', ])
@admin_required
def create():
    blog_entry = BlogEntry(evernote_url = request.form['evernote_url'])
    blog_entry.synchronize()
    db.session.add_then_commit(blog_entry)
    return redirect(url_for('admin.index'))


@blueprint.route('/delete/<int:id>/', methods = ['GET', ])
@admin_required
def delete(id):
    blog_entry = db.session.query(BlogEntry).get(id)
    if not blog_entry:
        abort(404)
    db.session.delete_then_commit(blog_entry)
    return redirect(url_for('admin.index'))


@blueprint.route('/synchronize/<int:id>/', methods = ['GET', ])
@admin_required
def synchronize(id):
    blog_entry = db.session.query(BlogEntry).get(id)
    if not blog_entry:
        abort(404)
    blog_entry.synchronize()
    db.session.commit()
    return redirect(url_for('admin.index'))
