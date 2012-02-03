========
EverBlog
========

Introduction
************
Everblog is named after Evernote, you can publish your Evernote notes to Everblog as blog entries.
When the notes in Evernote are updated, corresponding blog entries in Everblog are updated automatically.



Why Everblog ?
**************
Taking notes and writing blog entries are similar creative activities. You may want to publish some of your notes as blog entries.
We already have Evernote, a popular note taking application. It would be nice to have a blogging software which integrates well with Evernote.
Here comes Everblog!



Features
********
 - simple to setup and simple to use.
 - clear UI and clean HTML5 code.
 - minimal data storage. Most of the data is stored on third-party services such as Evernote and Disqus.
 - long-term maintained. I use it to power my own blog and I will continue to develop and maintain it.



Quick Start
***********
    git clone git://github.com/tylerlong/everblog.git && cd everblog
    pip install -r requires.txt
    python manage.py run_app

    open your browser and navigate to http://localhost:5000



Configuration and Customization
*******************************
    Most of the configurable items resides in everblog/__init__.py file
    If you want to change the default layout or menu, change everblog/templates/layout.html file



How to deploy ?
***************
The same as deploying any other wsgi based python websites.



Examples & Demos
****************
My blog: http://tylerlong.me



License
*******
Everblog is released under BSD license.



Feedback
********
Comments, suggestions, questions, free beer, t-shirts, kindles, ipads ... are all welcome!
Email: everblog.feedback@gmail.com
