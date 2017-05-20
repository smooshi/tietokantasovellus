WTF_CSRF_ENABLED = True
SECRET_KEY = 'life-is-a-mystery'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#config
DATABASE = 'database.db'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'default'
