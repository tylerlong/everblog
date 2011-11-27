# coding=utf-8
"""
    everblog.blueprints
    ~~~~~~~~~~~~~~~~~~~
    blueprints for the whole application
"""
import sys
from toolkit_library.inspector import PackageInspector
from everblog import app

packageInspector = PackageInspector(sys.modules[__name__])
all_blueprints = packageInspector.get_all_modules()

for blueprint in all_blueprints:
    #import blueprint
    exec('from everblog.blueprints import {0}'.format(blueprint))

    #register blueprint to app
    exec('app.register_blueprint({0}.blueprint)'.format(blueprint)) 
