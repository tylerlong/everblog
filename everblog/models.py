# coding=utf-8
"""
    wendaren.models
    ~~~~~~~~~~~~~~~
    Sqlalchemy database models
"""
from quick_orm.core import Database
from sqlalchemy import Column, String, DateTime, func

class DefaultModel(object):
    created = Column(DateTime, default = func.now())
    
metaclass = Database.MetaBuilder(DefaultModel)


class Article(object):
    __metaclass__ = metaclass
    evernote_guid = Column(String(64))
    evernote_key = Column(String(64))
