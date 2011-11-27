# coding=utf-8
"""
    everblog.blueprints.article
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Articles from evernote, Which will be converted to blog entries.
"""
import urllib2
from flask import Blueprint, render_template, abort
from everblog import db
from everblog.models import Article


blueprint = Blueprint('article', __name__)


@blueprint.route('/', methods = ['GET', ])
def list():
    articles = db.session.query(Article)
    return render_template('article/list.html', articles = articles)


@blueprint.route('/<int:id>/', methods = ['GET', ])
def read(id):
    article = db.session.query(Article).get(id)
    if not article:
        abort(404)
    url = 'https://www.evernote.com/shard/{0}/sh/{1}/{2}/note/{1}'.format(article.evernote_shard_id, article.evernote_guid, article.evernote_key)
    socket = urllib2.urlopen(url)
    article.content = socket.read().decode('utf-8')
    socket.close()
    return render_template('article/read.html', article = article)
