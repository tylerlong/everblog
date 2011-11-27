# coding=utf-8
"""
    manage
    ~~~~~~
    Like Django's manage.py, but simpler. Provides useful commands to manage the project
"""
import sys, subprocess
from toolkit_library.inspector import ModuleInspector
from everblog import db, fixtures


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


def show_tables():
    """Show all of the tables in database"""
    print db.engine.table_names()


def load_data():
    """Load data into database from fixtures.py"""
    db.load_data(fixtures)
    print 'Data loaded'


def recreate_tables_then_load_data():
    """recreate all tables and load the fixtures data"""
    drop_tables()
    create_tables()
    load_data()


def install_requirements():
    """Install required Python packages"""
    subprocess.call(['pip', 'install', '-r', 'requirements.txt', ])


if __name__ == '__main__':
    inspector = ModuleInspector(sys.modules[__name__])
    inspector.invoke(*sys.argv[1:])
