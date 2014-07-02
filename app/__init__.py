import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

if app.debug:
    print 'running in debug mode'
else:
    print 'NOT running in debug mode'


## setup logging
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('application.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

from app import views, models
