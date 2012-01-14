# coding=utf-8
"""
    wendaren.models
    ~~~~~~~~~~~~~~~
    Sqlalchemy database models
"""
import re, urllib2
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, DateTime, func, Integer, Enum
from toolkit_library.text_converter import TextConverter


evernote_url_pattern = re.compile('\.evernote\.com/shard/(?P<shard_id>[a-z]{1,2}\d{1,3})/sh/(?P<guid>[a-z0-9-]{24,48})/(?P<key>[a-z0-9]{24,40})')
evernote_title_pattern = re.compile('<title>(.+?)</title>')
chinese_character_pattern = re.compile(u'[\u4e00-\u9fa5]')


class DefaultModel(object):
    created = Column(DateTime, default = func.now())
    
metaclass = Database.MetaBuilder(DefaultModel)


class Article(object):
    """Represents an article"""
    __metaclass__ = metaclass
    evernote_url = Column(String(128), nullable = False, unique = True)
    title = Column(String(128), nullable = False)
    content = Column(Text, nullable = False)

    def synchronize(self):
        socket = urllib2.urlopen(self.evernote_url)
        data = socket.read().decode('utf-8')
        socket.close()
        match = evernote_title_pattern.search(data)
        self.title = match.group(1)        

        dct = evernote_url_pattern.search(self.evernote_url).groupdict()
        url = 'https://www.evernote.com/shard/{0}/sh/{1}/{2}/note/{1}'.format(dct['shard_id'], dct['guid'], dct['key'])
        socket = urllib2.urlopen(url)
        self.content = socket.read().decode('utf-8')
        socket.close()


class BlogEntry(Article):
    """Represents a note in evernote or a blog entry in everblog."""    
    snippet = Column(String(128))
    lang = Column(Enum('en', 'cn'), default = 'en')

    def synchronize(self):
        super(BlogEntry, self).synchronize()
        text_content = TextConverter.html_to_text(self.content)
        self.snippet = text_content[:128]
        if float(len(chinese_character_pattern.findall(text_content))) / len(text_content) > 0.1:
            self.lang = 'cn'


class Page(Article):
    "Represents a page in the website, such as the about page"
    order = Column(Integer)


Database.register()
