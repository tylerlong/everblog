# coding=utf-8
"""
    everblog.blueprints.tag
    ~~~~~~~~~~~~~~~~~~~~~~~
    tags for blog entries

"""
from flask import Blueprint, render_template, abort
from everblog import db
from everblog.models import Tag


blueprint = Blueprint('tag', __name__)


@blueprint.route('/tag/<name>/')
def read(name):
    tag = db.session.query(Tag).filter_by(name = name).first()
    if not tag:
        abort(404)
    return render_template('tag/read.html', tag = tag)


@blueprint.route('/tags/')
def list():
    tags = db.session.query(Tag).order_by(Tag.name)
    return render_template('tag/list.html', tags = tags)
