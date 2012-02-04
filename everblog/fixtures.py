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


blog_entries = [
    BlogEntry(evernote_url = 'http://www.evernote.com/shard/s68/sh/f69937b9-7cb1-414d-91ef-baca869dc263/f08695a8be5d370a4aba8ed8e141eb1e'),
    BlogEntry(evernote_url = 'http://www.evernote.com/shard/s68/sh/4d56d15c-250e-448e-8754-d7e17df66afe/72b4b597391d43cdf88948c3ad3c6446'),
]
for blog_entry in blog_entries:
    blog_entry.synchronize()


pages = [
    Page(order = 1, evernote_url = 'http://www.evernote.com/shard/s68/sh/f0df80b6-70c2-4858-b916-6e09b20a080d/b443c66aea7c40fe6ab68480f16094f8'),
    Page(order = 2, evernote_url = 'http://www.evernote.com/shard/s68/sh/04bfd5ca-3917-4484-977b-a622840990c9/a0bc16ee2749ea1a4e8814d5b9de02bd'),
]
for page in pages:
    page.synchronize()
