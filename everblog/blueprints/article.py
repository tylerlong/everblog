# coding=utf-8
"""
    everblog.blueprints.article
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Articles from evernote, Which will be converted to blog entries.
"""
from flask import Blueprint, render_template, abort
from everblog import db
from everblog.models import Article


blueprint = Blueprint('article', __name__)


@blueprint.route('/list/', methods = ['GET', ])
def list():
    articles = db.session.query(Article)
    return render_template('article/list.html', articles = articles)


@blueprint.route('/read/<int:id>/', methods = ['GET', ])
def read(id):
    article = db.session.query(Article).get(id)
    if not article:
        abort(404)
    return render_template('article/read.html', article = article)
