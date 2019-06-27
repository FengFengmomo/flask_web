from .database import Base
from sqlalchemy import Column, Integer, String,ForeignKey


class Users(Base):
    def __init__(self,userid,username,email,password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password

    __tablename__ = 'users'
    # __table__ = 'users'
    id = Column(Integer, primary_key=True)
    userid = Column(String(225), unique=True)
    username = Column(String(80), nullable=False)
    email = Column(String(320), nullable=False)
    password = Column(String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Admin(Base):

    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    userid = Column(String(225),unique = True)
    username = Column(String(80), nullable = False)
    email = Column(String(320), nullable = False)
    password = Column(String(32), nullable=False)

    def __init__(self,userid,username,email,password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Allow(Base):
    __doc__ = ''' 无账号可以使用的url '''
    __tablename__ = 'allow'
    id = Column(Integer, primary_key=True)
    urls = Column(String(200), unique=True)
    remark = Column(String(200))
    def __repr__(self):
        return '<User %r>' % self.urls


class Security(Base):
    __doc__ = '''账号权限列表'''
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True)
    userid = Column(ForeignKey('users.userid'))
    urls = Column(String(200), unique=True)

    def __repr__(self):
        return '<User %r>' % self.urls


class Task(Base):
    __doc__ = '''任务列表'''
    __tablename__ = 'task'
    userid = Column(String(20)) #ForeignKey('users.userid')
    taskid = Column(String(20), primary_key=True)
    jobid = Column(String(20), primary_key=True)
    urls = Column(String(225), unique=True)
    remark = Column(String(225))

    def __repr__(self):
        return '<User %r>' % self.urls


class Log(Base):
    __doc__ = '''日志信息'''
    __tablename__ = 'log'
    id = Column(Integer,autoincrement=True,primary_key=True)
    userid = Column(String(20))  # ForeignKey('users.userid')
    urls = Column(String(225), unique=True)
    params = Column(String(225))
    action = Column(String(225))
    remark = Column(String(225))