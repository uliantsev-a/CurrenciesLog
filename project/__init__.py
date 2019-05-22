import os

from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app)


config = {
    "development": "project.config.DevelopmentConfig",
    "testing": "project.config.TestingConfig",
    "default": "project.config.DevelopmentConfig"
}

config_name = os.getenv('FLASK_CONFIGURATION', 'default')

app.config.from_object(config[config_name])
app.config.from_pyfile('config.cfg', silent=True)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


# Setting logging
log_path = app.config['LOGFILE']
if not os.path.exists(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    f = open(log_path, 'a+')
    f.close()

handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=1)
log_level = logging.DEBUG if app.config['DEBUG'] else logging.INFO

handler.setLevel(log_level)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
                               '[in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)


# Load blueprints
from project.api.routes import mod_api  # noqa E402


app.register_blueprint(mod_api, url_prefix='/api')
