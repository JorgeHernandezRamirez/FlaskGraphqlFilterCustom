import json
import os
import unittest

from flask.ctx import AppContext
from graphene.test import Client

from app import app
from model import db, UserModel
from schema import schema


class UserTest(unittest.TestCase):

    FILTER_IN = """
        query{
          user(filters: {useridIn: [1, 2]}){
            edges{
              node{
                userid
                name
                surname
                age
              }
            }
          }
        }
    """

    FILTER_NE = """
        query{
          user(filters: {useridNe: 1}){
            edges{
              node{
                userid
                name
                surname
                age
              }
            }
          }
        }
    """

    FILTER_LIKE = """
        query{
          user(filters: {nameLike: "%os%"}){
            edges{
              node{
                userid
                name
                surname
                age
              }
            }
          }
        }
    """

    FILTER_LIKE_ALL_STRING = """
       query{
          user(filters: {nameLikeall: "Jo"}){
            edges{
              node{
                userid
                name
                surname
                age
              }
            }
          }
        }
    """

    FILTER_LIKE_ALL_NUMBER = """
        query{
          user(filters: {ageLikeall: "3"}){
            edges{
              node{
                userid
                name
                surname
                age
              }
            }
          }
        }
    """

    @staticmethod
    def _create_database_mock():
        db.drop_all()
        db.create_all()

    @staticmethod
    def _insert_users():
        db.session.add(UserModel(userid=1, name='Jorge', surname='Hernandez', age=32))
        db.session.add(UserModel(userid=2, name='Jose', surname='Hernandez', age=32))
        db.session.commit()

    @classmethod
    def setUpClass(cls) -> None:
        os.environ['FLASK_ENV'] = 'test'
        AppContext(app).push()
        UserTest._create_database_mock()
        UserTest._insert_users()

    def setUp(self):
        self.client = Client(schema)

    def _get_str_from_dict(self, dictionary: dict):
        return json.dumps(dictionary)

    def test_should_be_not_none_client(self):
        self.assertIsNotNone(self.client)

    def test_should_validate_in_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "1", "name": "Jorge", "surname": "Hernandez", "age": 32}}, {"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_IN))

    def test_should_validate_not_eq_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_NE))

    def test_should_validate_not_equal_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_NE))

    def test_should_validate_like_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_LIKE))

    def test_should_validate_like_all_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "1", "name": "Jorge", "surname": "Hernandez", "age": 32}}, {"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_LIKE_ALL_STRING))

    def test_should_validate_like_all_operator(self):
        self.assertEqual(
            {"data": {"user": {"edges": [{"node": {"userid": "1", "name": "Jorge", "surname": "Hernandez", "age": 32}}, {"node": {"userid": "2", "name": "Jose", "surname": "Hernandez", "age": 32}}]}}},
            self.client.execute(self.FILTER_LIKE_ALL_NUMBER))

if __name__ == '__main__':
    unittest.main()
