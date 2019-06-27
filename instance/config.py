from datetime import timedelta
import os
# SECRET_KEY =' dev123'
# PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
#set FLASK_APP=APPNAME  export FLASK_APP=APPNAME
#set FLASK_ENV=development export FLASK_ENV=development
#flask run --host=0.0.0.0
UPLOAD_FOLDER = '/uploads'
DEBUG = True
# SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
SECRET_KEY = 'flask development'
# DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
MAX_CONTENT_LENGTH = 1600 * 1024 * 1024 #1600M
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qq125680..@localhost:3306/test2?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv','xslx'])