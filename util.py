from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# app.config.from_object('yourapplication.default_settings')
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # global db
    CORS(app,supports_credentials=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # global db
    # db = SQLAlchemy(app)

    # db.create_all()
    # g.db = db
    from views import register_views
    app = register_views(app)

    return app
