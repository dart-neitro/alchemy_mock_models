import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
        Column,
        Integer,
        String,
)
from sqlalchemy.ext.declarative import declarative_base

from project.models import Base, User, SQLServer


class MyTest(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)
        self.session.add(User('user1', 'user1@email.local'))
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_panel(self):
        user = User('user1', 'user1@email.local')
        user.id = 1
        expected = [user]
        result = self.session.query(User).all()

        expected = [x.to_dict() for x in expected]
        result = [x.to_dict() for x in result]
        self.assertEqual(result, expected)


TestBase = declarative_base()


class TestUser(TestBase):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(Integer, nullable=False)

    __init__ = User.__init__
    __repr__ = User.__repr__
    to_dict = User.to_dict


class TestSQLServer(SQLServer):
    def __init__(self):
        self.connect_string = 'sqlite:///:memory:'
        self.session = None

    def connect(self):
        engine = create_engine(self.connect_string)
        TestBase.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.engine = engine








class SQLServerTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self):
        Base.metadata.drop_all(self.sql_server.engine)

    @mock.patch('project.models.User', TestUser)
    @mock.patch('project.models.Base', TestBase)
    def test_functional(self):
        self.sql_server = TestSQLServer()
        self.sql_server.connect()

        user = TestUser('user1', 11)
        user.id = 1
        expected = user.to_dict()

        sql_server = self.sql_server
        sql_server.add_user(name='user1', email=11)
        user = sql_server.get_user(1)
        result = user.to_dict()

        self.assertEqual(expected, result)
