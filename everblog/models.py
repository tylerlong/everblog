# coding=utf-8
"""
    wendaren.models
    ~~~~~~~~~~~~~~~
    Sqlalchemy database models
"""
import re, urllib2, json, datetime
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, DateTime, func, Integer, Enum
from toolkit_library.text_converter import TextConverter


evernote_data_pattern = re.compile('(?<=Evernote\.WebClient\.Note = )\{.+?\}(?=;\s+?</script>)')
chinese_character_pattern = re.compile(u'[\u4e00-\u9fa5]')


__metaclass__ = Database.DefaultMeta


class Article:
    """Represents an article"""
    created = Column(DateTime, nullable = False)
    updated = Column(DateTime, nullable = False)
    published = Column(DateTime, default = func.now())
    evernote_url = Column(String(128), nullable = False, unique = True)
    title = Column(String(128), nullable = False)
    content = Column(Text, nullable = False)

    def synchronize(self):
        data = urllib2.urlopen(self.evernote_url).read().decode('UTF-8')
        data = evernote_data_pattern.search(data).group()
        dict_ = json.loads(data.replace('\<', '<').replace('\>', '>'))
        self.title = dict_['title']
        self.content = dict_['content']
        self.created = datetime.datetime.fromtimestamp(dict_['created']/1000)
        self.updated = datetime.datetime.fromtimestamp(dict_['updated']/1000)


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
