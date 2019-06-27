import sqlite3
from flask import current_app,g
from app import app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory =sqlite3.Row
    return g.db


def close_db(e = None):
    db = g.pop('db',None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def init_app(app):
    init_db()
    app.teardown_appcontext(close_db)