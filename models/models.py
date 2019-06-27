from util import db
# from flask_sqlalchemy import SQLAlchemy
# from flask import g
# db = g.db
# db = SQLAlchemy()
class Users(db.Model):
    def __init__(self,userid,username,email,password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(225), unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Admin(db.Model):

    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(225),unique = True)
    username = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(320), nullable = False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self,userid,username,email,password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Allow(db.Model):
    __doc__ = ''' 无账号可以使用的url '''
    __tablename__ = 'allow'
    id = db.Column(db.Integer, primary_key=True)
    urls = db.Column(db.String(200), unique=True)
    remark = db.Column(db.String(200))
    def __repr__(self):
        return '<User %r>' % self.urls


class Security(db.Model):
    __doc__ = '''账号权限列表'''
    __tablename__ = 'security'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.ForeignKey('users.userid'))
    urls = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return '<User %r>' % self.urls


class Task(db.Model):
    __doc__ = '''任务列表'''
    __tablename__ = 'task'
    userid = db.Column(db.String(20)) #db.ForeignKey('users.userid')
    taskid = db.Column(db.String(20), primary_key=True)
    jobid = db.Column(db.String(20), primary_key=True)
    urls = db.Column(db.String(225), unique=True)
    remark = db.Column(db.String(225))

    def __repr__(self):
        return '<User %r>' % self.urls


class Log(db.Model):
    __doc__ = '''日志信息'''
    __tablename__ = 'log'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    userid = db.Column(db.String(20))  # db.ForeignKey('users.userid')
    urls = db.Column(db.String(225), unique=True)
    params = db.Column(db.String(225))
    action = db.Column(db.String(225))
    remark = db.Column(db.String(225))