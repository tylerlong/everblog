# coding=utf-8
"""
    manage
    ~~~~~~
    Like Django's manage.py, but simpler. Provides useful commands to manage the project
"""
import os, sys, subprocess
from everblog import db


def show_tables():
    """Show all of the tables in database"""
    print db.engine.table_names()


def drop_tables():
    """Drop all tables in database"""
    db.drop_tables()
    print 'Tables dropped'


def create_tables():
    """Create tables according to models"""
    db.create_tables()
    print 'Tables created'


def recreate_tables():
    """Drop all tables then recreate them"""
    drop_tables()
    create_tables()


def load_data():
    """Load data into database from fixtures.py"""
    from everblog import fixtures
    db.load_data(fixtures)
    print 'Data loaded'


def recreate_tables_then_load_data():
    """Recreate all tables and load the fixtures data"""
    drop_tables()
    create_tables()
    load_data()


def run_app():
    """Run the web application"""
    from everblog import app
    if len(sys.argv) < 2:
        subprocess.call([sys.executable, 'manage.py', 'run_app'])
    else:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port = port)


if __name__ == '__main__':
    from toolkit_library.inspector import ModuleInspector
    inspector = ModuleInspector(sys.modules[__name__])
    inspector.invoke(*sys.argv[1:])