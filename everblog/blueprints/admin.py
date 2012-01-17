# coding=utf-8
"""
    everblog.blueprints.admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    site administration
"""
from flask import Blueprint, request, render_template, abort, session, redirect, url_for
from everblog import app, db
from everblog.blueprints import admin_required
from everblog.models import Article, BlogEntry


blueprint = Blueprint('admin', __name__)


@blueprint.route('/login/', methods = ['GET', 'POST', ])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    username = request.form['username']
    password = request.form['password']
    if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
        session['admin'] = True
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html')


@blueprint.route('/logout/', methods = ['GET', ])
def logout():
    """logout"""
    session.clear()
    return redirect(url_for('blog_entry.list'))


@blueprint.route('/admin/', methods = ['GET', ])
@admin_required
def index():
    """Administration home page"""
    blog_entries = db.session.query(BlogEntry)
    return render_template('admin/index.html', blog_entries = blog_entries)


@blueprint.route('/sync/', methods = ['GET', ])
def synchronize():
    """synchronize contents with Evernote"""
    articles = db.session.query(Article)
    for article in articles:
        article.synchronize()
    db.session.commit()
    return 'Synchronization finished successfully. You may close this page.'
