from flaskr.admin import admin
from flaskr.user import user
from tools import tools
from flask import g,url_for
from manage.manage import manage
from models.database import db_session,init_db
from chromecontroller.flask_and_asyncio import tasks

def register_views(app):
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(tools, url_prefix='/')
    app.register_blueprint(manage,url_prefix='/manage')
    app.register_blueprint(tasks,url_prefix='/tasks')
    @app.teardown_appcontext
    def close_db(e = None):
        db_session.remove()
        db = g.pop('db', None)
        if db is not None:
            db.close()

    @app.before_first_request
    def init_app():
        init_db()
    with app.test_request_context():
        # print(url_for('index'))
        print(url_for('tools.login1', post_id="123"))
        print(url_for('tools.hello', name='/net'))
        print(url_for('static', filename='data.json'))
    return app

# url_for('admin.index')
# url_for('.index') 跳到同一个蓝图下的url