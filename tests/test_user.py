from unittest import TestCase

from mongoengine import connect, disconnect
from starlette.testclient import TestClient

from app import app
from app.models.user import Users

client = TestClient(app)


class TestPerson(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/cobadb')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_thing(self):
        name = "Ibie"
        pers = Users(name=name)
        pers.save()

        fresh_pers = Users.objects(name=name).first()
        assert fresh_pers.name == name

    def test_callName(self):
        name = "Ibie"
        pers = Users(name=name)
        pers.save()

        fresh_pers = Users.objects(name=name).first()
        assert fresh_pers.name == name

    def test_callName2(self):
        name = "Ibie"
        pers = Users(name=name)
        pers.save()

        fresh_pers = Users.objects(name=name).first()
        assert fresh_pers.name == name

    def test_create_user(self):
        response = client.post("/users", json={"name": "hudya"})
        user = Users.objects.get(name="hudya")

        assert response.status_code == 200
        assert user.name == "hudya"
