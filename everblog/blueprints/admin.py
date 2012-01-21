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
    """login"""
    if request.method == 'GET':
        return render_template('admin/login.html')
    if request.form['username'] == app.config['ADMIN_USERNAME'] and request.form['password'] == app.config['ADMIN_PASSWORD']:
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
    """administration home page"""
    blog_entries = db.session.query(BlogEntry).order_by(BlogEntry.created.desc())
    return render_template('admin/index.html', blog_entries = blog_entries)
