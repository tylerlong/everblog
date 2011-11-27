# coding=utf-8
"""
    wendaren.models
    ~~~~~~~~~~~~~~~
    Sqlalchemy database models
"""
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, DateTime, func


class DefaultModel(object):
    created = Column(DateTime, default = func.now())
    
metaclass = Database.MetaBuilder(DefaultModel)


class Article(object):
    """Represents a note in evernote or a blog entry in everblog."""
    __metaclass__ = metaclass
    evernote_shard_id = Column(String(32))
    evernote_guid = Column(String(64))
    evernote_key = Column(String(64))
    title = Column(String(128))
    snippet = Column(String(512))
    content = Column(Text)
