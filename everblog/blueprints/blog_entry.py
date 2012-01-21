# coding=utf-8
"""
    everblog.blueprints.blog_entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Notes from evernote, Which will be converted to blog entries.
"""
import hashlib
from time import mktime
from urlparse import urljoin
from flask import Blueprint, render_template, abort, redirect, url_for, request, make_response
from wsgiref.handlers import format_date_time
from werkzeug.contrib.atom import AtomFeed
from everblog import app, db
from everblog.models import BlogEntry
from everblog.blueprints import admin_required

DEFAULT_LANG = app.config['DEFAULT_LANG']
PAGE_SIZE = app.config['PAGE_SIZE']

blueprint = Blueprint('blog_entry', __name__)

@blueprint.route('/<regex("[a-z]{2}"):lang>/page/<int:page>/', methods = ['GET', ])
def list_lang_page(lang, page):
    """blog entry list, filtered by language and page number"""
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
    """blog entry list, filtered by language, show the first page"""
    return list_lang_page(lang, 1)

@blueprint.route('/page/<int:page>/', methods = ['GET', ])
def list_page(page):
    """blog entry list, filtered by page number, show entries in the default language"""
    return list_lang_page(DEFAULT_LANG, page)

@blueprint.route('/', methods = ['GET', ])
def list():
    """blog entry list, show the first page of entries in the default language"""
    return list_lang(DEFAULT_LANG)


@blueprint.route('/<int:id>/', methods = ['GET', ])
def read(id):
    """show a blog entry"""
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
    """create a blog entry"""
    blog_entry = BlogEntry(evernote_url = request.form['evernote_url'])
    blog_entry.synchronize()
    db.session.add_then_commit(blog_entry)
    return redirect(url_for('admin.index'))


@blueprint.route('/<regex("[a-z]{2}"):lang>/feed.atom', methods = ['GET', ])
def lang_feed(lang):
    """generate atom feed for blog entries in the specific language"""
    blog_entries = db.session.query(BlogEntry).filter_by(lang = lang).order_by(BlogEntry.created.desc()).limit(PAGE_SIZE)
    updated = blog_entries.first().created if blog_entries.count() > 0 else ''

    etag = '"{0}"'.format(hashlib.sha256(str(updated)).hexdigest())
    if request.headers.get('If-None-Match', '') == etag:
        return '', 304
    last_modified = format_date_time(mktime(updated.timetuple()))
    if request.headers.get('If-Modified-Since', '') == last_modified:
        return '', 304

    title = app.config['BLOG_OWNER'] + "'s Thoughts and Writings"
    if lang == 'cn':
        title = app.config['BLOG_OWNER'] + u'的博客'
    feed = AtomFeed(title = title, 
                    url = request.url_root, 
                    feed_url = request.url, 
                    author = app.config['BLOG_OWNER'])
    if updated:
        feed.updated = updated
    for blog_entry in blog_entries:
        feed.add(title = blog_entry.title, 
                 content = unicode(blog_entry.content),
                 content_type = 'html',
                 author = app.config['BLOG_OWNER'],
                 url = urljoin(request.url_root, url_for('blog_entry.read', id = blog_entry.id)),
                 updated = blog_entry.updated,
                 published = blog_entry.created)
    
    response = feed.get_response()
    response.headers['ETag'] = etag
    response.headers['Last-Modified'] = last_modified
    return response


@blueprint.route('/feed.atom', methods = ['GET', ])
def feed():
    """generate atom feed for blog entries in the default language"""
    return lang_feed(DEFAULT_LANG)
