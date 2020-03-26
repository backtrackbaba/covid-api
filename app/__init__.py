import os

from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from walrus import Database

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
redis_db = Database(host=os.environ.get('CACHE_REDIS_HOST'), port=os.environ.get('CACHE_REDIS_PORT'),
                    db=os.environ.get('CACHE_REDIS_DB'), password=os.environ.get('CACHE_REDIS_PASSWORD'))
cache = redis_db.cache(default_timeout=int(os.environ.get('CACHE_REDIS_TIMEOUT')))
basic_auth = BasicAuth()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)

    from app.api.v1 import bp as main_bp
    app.register_blueprint(main_bp)

    from app.common import bp as common_bp
    app.register_blueprint(common_bp)

    from app.protected import bp as protected_bp
    app.register_blueprint(protected_bp)

    return app
