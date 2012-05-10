Everblog
========


|

Introduction
------------
Everblog is named after Evernote, you can publish your Evernote notes to Everblog as blog entries.

When the notes in Evernote are updated, corresponding blog entries in Everblog are updated automatically.


|

Why Everblog ?
--------------
Taking notes and writing blog entries are similar creative activities. You may want to publish some of your notes as blog entries.

We already have Evernote, a popular note taking application. It would be nice to have a blogging software which integrates well with Evernote.

Here comes Everblog!


|

Features
--------
- simple to setup and simple to use.
- clear UI and clean HTML5 code.
- minimal data storage. Most of the data is stored on third-party services such as Evernote and Disqus.
- support atom feeds, tag clouds and google analytics.
- long-term maintained. I use it to power my own blog and I will continue to develop and maintain it.


|

Quick Start
-----------

::

    git clone git://github.com/tylerlong/everblog.git && cd everblog
    edit everblog/__init__.py and change the settings.
    pip install -r requirements.txt
    python manage.py recreate_tables_then_load_data
    python manage.py run_app

open your browser and navigate to http://localhost:5000


|

Configuration and Customization
-------------------------------
 - Most of the configurable items resides in everblog/__init__.py file
 - If you want to change the default layout or menu, change everblog/templates/layout.html file


|

How to deploy ?
---------------
I wrote a tutorial(In Chinese): http://www.tylerlong.me/1336566394/


|

Examples & Demos
----------------
http://everblog.herokuapp.com, administrator account & password: admin/password


|

License
-------
Everblog is released under BSD license.


|

Feedback
--------
Comments, suggestions, questions, free beer, t-shirts, kindles, ipads ... are all welcome!

Email: everblog.feedback@gmail.com


|

todo list
---------
1. investigate sharing a folder in Evernote
#. pagination for admin pages
#. support full-text searching - index bucket?
#. add event flow? such as github flow on this man's page: http://scottchacon.com/
#. add "todo". create todo items, can mark them as finished or postponed or given up. track the time. write comments. write summary.
#. auto generate resume according to the contents of the blog.