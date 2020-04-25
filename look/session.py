from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from look.model.user import User as UserModel

def init_session():
    print("init_session")
    engine = create_engine('mysql+mysqldb://root:root@localhost:3306/codedu?charset=utf8')

    Session = sessionmaker(bind=engine)

    UserModel.metadata.create_all(engine)

    return Session