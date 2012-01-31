# coding=utf-8
"""
    everblog.blueprints.article
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Article, base model for page and blog entry.
"""
from flask import abort, redirect, url_for, Blueprint
from everblog import db
from everblog.models import Article, Tag
from everblog.blueprints import admin_required


blueprint = Blueprint('article', __name__)


@blueprint.route('/sync/<int:id>/', methods = ['GET', ])
def synchronize(id):
    """synchronize an article with Evernote"""
    article = db.session.query(Article).get(id)
    if not article:
        abort(404)
    article.synchronize()
    db.session.commit()
    return 'Synchronization finished successfully. <a href="javascript:self.close()" >Close</a> this window.'
    

@blueprint.route('/sync/', methods = ['GET', ])
def synchronize_all():
    """synchronize all of the articles with Evernote"""
    for article in db.session.query(Article):
        article.synchronize()
        db.session.commit()
    for tag in db.session.query(Tag):
        if tag.articles.count() <= 0:
            db.session.delete_then_commit(tag)
    return 'Synchronization finished successfully. <a href="javascript:self.close()" >Close</a> this window.'


@blueprint.route('/delete/<int:id>/', methods = ['GET', ])
@admin_required
def delete(id):
    """delete an article"""
    article = db.session.query(Article).get(id)
    if not article:
        abort(404)
    db.session.delete_then_commit(article)
    return redirect(url_for('admin.index'))
