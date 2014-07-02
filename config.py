import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

UPLOAD_FOLDER = '/home/tcollins/dev/perf/.data-uploads'

## dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/perf'
SQLALCHEMY_ECHO = False