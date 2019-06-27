from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from instance.config import SQLALCHEMY_DATABASE_URI
# engine = create_engine("mysql+pymysql://root:qq125680..@localhost:3306/test2?charset=utf8", convert_unicode=True)
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
# with app.app_context():
#     engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # 在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地
    # 在 metadata 中注册。否则，您将不得不在第一次执行 init_db() 时
    # 先导入他们。
    import models.models2
    Base.metadata.create_all(bind=engine)