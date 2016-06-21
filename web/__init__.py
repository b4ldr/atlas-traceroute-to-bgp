from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging

PYASN_FILE = 'ipasn_db.dat'
app        = Flask(__name__)
db         = SQLAlchemy(app)
Bootstrap(app)
app.config.from_object('config')

logging.basicConfig(level=logging.DEBUG)

from web import views
from web import models
