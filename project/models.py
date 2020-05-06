from sqlalchemy import (
        Column,
        Integer,
        String,
)
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return (
            "<User('{self.name}', '{self.email}')>".format(self=self)
        )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
        )


class SQLServer:
    def __init__(self, connect_string, very_need_arg):
        self.connect_string = connect_string
        self.very_need_arg = very_need_arg
        self.session = None

    def connect(self):
        engine = create_engine(self.connect_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_user(self, name='user1', email='user1@email.global'):
        self.session.add(User(name, email))
        self.session.commit()

    def get_user(self, id):
        return self.session.query(User).get(id)
