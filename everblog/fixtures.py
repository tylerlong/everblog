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
    evernote_guid = 'dbe815e0-2326-4319-8acb-a1f2a1dce991',
    evernote_key = '9500cbb022e2239df5f287ae89a664c7'
))
