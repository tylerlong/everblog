# coding=utf-8
"""
    everblog.models
    ~~~~~~~~~~~~~~~
    quick_orm database models
"""
import re, json, datetime, anydbm
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, DateTime, func, Integer, Enum
from toolkit_library.text_converter import TextConverter
from toolkit_library.web_client import WebClient
from toolkit_library.encryption import Encryption
from everblog import db, app


evernote_data_pattern = re.compile('(?<=Evernote\.WebClient\.Note = )\{.+?\}(?=;\s+?</script>)')
chinese_character_pattern = re.compile(u'[\u4e00-\u9fa5]')
img_url_pattern = re.compile(' src="(https?://.+?\.(?:png|jpg|jpeg|gif))"')


__metaclass__ = Database.DefaultMeta


class Article:
    """Represents an article"""
    uid = Column(Integer, nullable = False, unique = True, index = True)
    created = Column(DateTime, nullable = False, unique = True, index = True)
    updated = Column(DateTime, nullable = False)
    published = Column(DateTime, nullable = False, default = func.now())
    evernote_url = Column(String(128), nullable = False, unique = True)
    title = Column(String(128), nullable = False)
    content = Column(Text, nullable = False)

    def synchronize(self):
        data = WebClient.download_binary(self.evernote_url).decode('UTF-8')
        data = evernote_data_pattern.search(data).group()
        dict_ = json.loads(data.replace('\<', '<').replace('\>', '>'))
        self.title = dict_['title']
        self.content = dict_['content']
        match = img_url_pattern.search(self.content)
        if match:
            try:
                dbm = anydbm.open(app.config['IMAGE_CACHE'], 'c')
                for img_url in match.groups():
                    key = Encryption.computer_hashcode(img_url)
                    value = WebClient.download_binary(img_url)
                    dbm[key] = value
                    self.content = self.content.replace(img_url, '/image/{0}/'.format(key))
            finally:
                dbm.close()
        self.uid = dict_['created'] / 1000
        self.created = datetime.datetime.utcfromtimestamp(self.uid)
        self.updated = datetime.datetime.utcfromtimestamp(dict_['updated'] / 1000)
        self.tags = []
        if 'tagNames' in dict_:
            for tagName in dict_['tagNames']:
                tag = db.session.query(Tag).filter_by(name = tagName).first()
                tag = tag if tag else Tag(name = tagName)
                self.tags.append(tag)


class BlogEntry(Article):
    """Represents a note in evernote or a blog entry in everblog."""
    snippet = Column(String(128), nullable = False)
    lang = Column(Enum('en', 'cn'), nullable = False, index = True, default = 'en')

    def synchronize(self):
        super(BlogEntry, self).synchronize()
        text_content = TextConverter.html_to_text(self.content)
        self.snippet = text_content[:128]
        if float(len(chinese_character_pattern.findall(text_content))) / len(text_content) > 0.1:
            self.lang = 'cn'


class Page(Article):
    "Represents a page in the website, such as the about page"
    order = Column(Integer, nullable = False, default = 1)


@Database.many_to_many(Article)
class Tag:
    """represents a tag in Evernote"""
    name = Column(String(64), nullable = False, index = True, unique = True)


Database.register()
