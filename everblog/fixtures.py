# coding=utf-8
"""
    everblog.fixtures
    ~~~~~~~~~~~~~~~~~
    Contains fixtures data to be inserted into database
"""
import everblog.models
from toolkit_library.inspector import ModuleInspector 

moduleInspector = ModuleInspector(everblog.models)
exec(moduleInspector.import_all_classes_statement())


articles = []
articles.append(Article(
    evernote_shard_id = 's68',
    evernote_guid = 'dbe815e0-2326-4319-8acb-a1f2a1dce991',
    evernote_key = '9500cbb022e2239df5f287ae89a664c7',
    title = u'如何部署一个基于python wsgi 的网站到linux系统',
    snippet = u'如何部署一个基于python wsgi的网站到linux系统 Python wsgi是一个标准接口, 大部分的web server(比如apache, nginx等)都支持这一接口(直接支持或者通过扩展的方式支持), 大部分的python web框架(比如django, pyramid等)也都支持这一接口. 于是它带来的好处就是: 几乎所有的python web框架都能够部署到几乎所有的web se...'
))
