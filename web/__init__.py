from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))

PYASN_FILE = os.path.join(basedir,'ipasn_db.dat')
app        = Flask(__name__)
db         = SQLAlchemy(app)
Bootstrap(app)
app.config.from_object('config')
app.secret_key = '@U@5K6.B7ppi_ShyyhrH7C@}X&F/LN<pidu]C1G'

logging.basicConfig(level=logging.DEBUG)

from web import views
from web import models
