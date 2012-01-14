# coding=utf-8
"""
    everblog.blueprints.blog_entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Notes from evernote, Which will be converted to blog entries.
"""
from flask import Blueprint, render_template, abort, redirect, url_for, request
from everblog import db
from everblog.models import BlogEntry
from everblog.blueprints import admin_required


blueprint = Blueprint('blog_entry', __name__)


@blueprint.route('/', methods = ['GET', ])
def list():
    blog_entries = db.session.query(BlogEntry).filter_by(lang = 'en').order_by(BlogEntry.created.desc())
    return render_template('blog_entry/list.html', items = blog_entries)


@blueprint.route('/cn/', methods = ['GET', ])
def list_cn():
    blog_entries = db.session.query(BlogEntry).filter_by(lang = 'cn').order_by(BlogEntry.created.desc())
    return render_template('blog_entry/list.html', items = blog_entries)


@blueprint.route('/<int:id>/', methods = ['GET', ])
def read(id):
    blog_entry = db.session.query(BlogEntry).get(id)
    if not blog_entry:
        abort(404)
    return render_template('blog_entry/read.html', blog_entry = blog_entry)


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
