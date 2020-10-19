from unittest import TestCase

import json
from bson import ObjectId

from mongoengine import connect, disconnect
from starlette.testclient import TestClient

from app import app
from app.models.user import Users

client = TestClient(app)


class TestUser(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/mocking_db')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_insert_user(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})
        assert response.status_code == 200

        user = Users.objects(name=name).first()
        assert user.name == name

    def test_insert_user_with_long_name(self):
        name = "SngQ8CL1kqtowD4rl1kYrWG2WmLhvB6HQ7exaY3a5fFkG6LPBn4s" \
               "Gtc5HZw7QHiQtsLKrAX7G7wBPp5of6utYDeTLllNPMJfE1m"

        response = client.post("/users", json={"name": name})
        assert response.status_code == 200

        user = Users.objects.get(name=name)
        assert user.name == name

    def test_insert_user_with_empty(self):
        name = ""

        response = client.post("/users", json={"name": name})
        assert response.status_code == 400

    def test_insert_user_without_name_parameter(self):
        response = client.post("/users", json={})
        assert response.status_code == 400

    def test_update_user(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']

        new_name = "Kiddy"
        response = client.put(f"/users/{id}", json={"name": new_name})
        assert response.status_code == 200

        user = Users.objects(id=id).first()
        assert user.name == new_name

    def test_update_user_with_long_name(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']

        new_name = "SngQ8CL1kqtowD4rl1kYrWG2WmLhvB6HQ7exaY3a5fFkG6LPBn4s" \
                   "Gtc5HZw7QHiQtsLKrAX7G7wBPp5of6utYDeTLllNPMJfE1m"
        response = client.put(f"/users/{id}", json={"name": new_name})
        assert response.status_code == 200

        user = Users.objects(id=id).first()
        assert user.name == new_name

    def test_update_user_with_wrong_id(self):
        name = "Hudya"

        client.post("/users", json={"name": name})
        id = str(ObjectId())

        new_name = "Kiddy"
        response = client.put(f"/users/{id}", json={"name": new_name})
        assert response.status_code == 400

        user = Users.objects(id=id).first()
        assert user is None

    def test_update_user_without_name(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']

        response = client.put(f"/users/{id}", json={})
        assert response.status_code == 400

        user = Users.objects(id=id).first()
        assert user.name == name

    def test_update_user_with_empty_name(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']

        response = client.put(f"/users/{id}", json={"name": ""})
        assert response.status_code == 400

        user = Users.objects(id=id).first()
        assert user.name == name

    def test_delete_user(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']

        response = client.delete(f"/users/{id}")
        assert response.status_code == 200

        user = Users.objects(id=id).first()
        assert user is None

    def test_delete_user_wrong_id(self):
        name = "Hudya"

        response = client.post("/users", json={"name": name})

        res = response.text
        res = json.loads(res)
        id = res['values']['id']
        fake_id = str(ObjectId())

        response = client.delete(f"/users/{fake_id}")
        assert response.status_code == 400

        user = Users.objects(id=id).first()
        assert user.name == name

        user = Users.objects(id=fake_id).first()
        assert user is None
