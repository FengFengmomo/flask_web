from flask import Blueprint,render_template,session, request, flash,current_app
from werkzeug.security import generate_password_hash
from datetime import timedelta
from models.models2 import Users
from models.database import db_session
# manage = Blueprint('manage',__name__, template_folder='templates',static_folder='static')
manage = Blueprint('manage',__name__)


@manage.route("/loginpage")
def login_page():
    # return render_template("/manage/manage/register.html")
    return render_template("manage/login.html")


@manage.route("/login", methods =['GET','POST'])
def login():
    '''设置session时间'''
    if (request.method == 'POST'):
        id = request.form['ids']
        # ids = request.args.get('ids', '')
        password = request.form['password']
        if id == '' or password == '':
            flash("id or password can't be null")
        user = Users.query.filter(id == 1).first()
        user2 = Users.query.get(2)

        # print(ids)
        print(user)
        print(user.users_id)
        print(user.users_username)
        print(user.users_email)
        print(user.users_password)
        # db.session.query("asfs")
        session.clear()
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=10)
        # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
        session['userid']='123'
    return "login successfully"


@manage.route("/register",methods=['POST'])
def register():
    userid = request.form['userid']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if userid is not None and username is not None and password is not None:
        user = Users(userid,username,email,generate_password_hash(password))
        db_session.add(user)
        db_session.commit()
        return render_template('manage/login.html')
    flash("账号密码不能为空",'error')
    return render_template('manage/register.html')