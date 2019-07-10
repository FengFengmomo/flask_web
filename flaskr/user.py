from flask import Blueprint,render_template, request
from models.models2 import Users
# from util import db
user = Blueprint('users',__name__)
@user.route('/index')
def index():
    return render_template('user/index.html')

@user.route('/add/',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        p_user = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)

        if not p_user or not p_email or not p_password:
            return 'input error'

        newobj = Users(username=p_user, email=p_email, password=p_password)
        # db = g.db
        db.session.add(newobj)
        db.session.commit()
        users = Users.query.all()
        return render_template('user/add.html',users=users)
    users = Users.query.all()
    return render_template('user/add.html',users=users)

@user.route('/show')
def show():
    return 'user_show'