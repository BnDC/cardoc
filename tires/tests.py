import json
import bcrypt
import jwt

from django.test   import TestCase, Client
from unittest.mock import MagicMock, patch

from users.models import User
from tires.models import Trim, Tire
from tires.mocked import mocked_data_success, mocked_data_fail
from my_settings  import SECRET_KEY, ALGORITHM

class UserTest(TestCase):
    def setUp(self):
        self.password     = bcrypt.hashpw("abc1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm = ALGORITHM)

        user_list = [
            User(
                id       = 1,
                email    = "user1@naver.com",
                password = self.password
            ),
            User(
                id       = 2,
                email    = "user2@naver.com",
                password = self.password
            ),
            User(
                id       = 3,
                email    = "user3@naver.com",
                password = self.password
            ),
            User(
                id       = 4,
                email    = "user4@naver.com",
                password = self.password
            ),
            User(
                id       =5,
                email= "user5@naver.com",
                password = self.password
            ),
            User(
                id       = 6,
                email    = "user6@naver.com",
                password = self.password
            )
        ]

        User.objects.bulk_create(user_list)

        tire_list = [
            Tire(
                id           = 1,
                width        = 205,
                aspect_ratio = 60,
                size         = 15,
            ),
            Tire(
                id           = 2,
                width        = 205,
                aspect_ratio = 55,
                size         = 16,
            ),
        ]

        Tire.objects.bulk_create(tire_list)

    def tearDown(self):
        User.objects.all().delete()
        Tire.objects.all().delete()

    @patch('tires.utils.requests')
    def test_tire_save_post_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return mocked_data_success

        mocked_requests.get = MagicMock(return_value =MockedResponse())

        data = [{
            "id": "user1@naver.com",
            "trimId" : 5000,
            }
        ]

        response = client.post("/tires", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.status_code, 200)
    
    @patch('tires.utils.requests')
    def test_tire_save_post_invaild_user_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return mocked_data_success

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        data = [{
            "id"     : "bad@naver.com",
            "trimId" : 5000,
            }
        ]

        response = client.post("/tires", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.status_code, 400)
    
    @patch('tires.utils.requests')
    def test_tire_save_post_invaild_trim_id_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return mocked_data_fail

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        data = [{
            "id"     : "user2@naver.com",
            "trimId" : 99999999,
            }
        ]

        response = client.post("/tires", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.status_code, 400)

    @patch('tires.utils.requests')
    def test_tire_save_post_empty_data_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return mocked_data_success

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        data = [
        
        ]

        response = client.post("/tires", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.status_code, 400)

    @patch('tires.utils.requests')
    def test_tire_save_post_too_much_request_fail(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code = 200 
            
            def json(self):
                return mocked_data_success

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        data = [{
            "id" : "user1@naver.com",
            "trimId" : 1,
            },
            {
            "id" : "user2@naver.com",
            "trimId" : 2,
            },
            {
            "id" : "user3@naver.com",
            "trimId" : 3,
            },
            {
            "id" : "user4@naver.com",
            "trimId" : 4,
            },
            {
            "id" : "user5@naver.com",
            "trimId" : 5,
            },
            {
            "id" : "user6@naver.com",
            "trimId" : 6,
            },
        
        ]

        response = client.post("/tires", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.status_code, 400)

    def test_user_tire_get_success(self):

        user = User.objects.get(id = 2)

        trim1 = Trim.objects.create(
            trim_id       = 1,
            front_tire_id = 1,
            back_tire_id  = 1,
        )
        trim2 = Trim.objects.create(
            trim_id       = 2,
            front_tire_id = 2,
            back_tire_id  = 2,
        )

        user.trim.add(trim1)
        user.trim.add(trim2)
        user.save()

        client = Client()
        headers = {"HTTP_Authorization" : self.access_token}
        response = client.get("/tires", **headers)

        Trim.objects.all().delete()

        self.assertEqual(response.json(), {
                    "result": [
                        {
                            "trim_id": 1,
                            "front-tire": {
                                "width": 205,
                                "aspect_ratio": 60,
                                "size": 15
                            },
                            "rear-tire": {
                                "width": 205,
                                "aspect_ratio": 60,
                                "size": 15
                            }
                        },
                        {
                            "trim_id": 2,
                            "front-tire": {
                                "width": 205,
                                "aspect_ratio": 55,
                                "size": 16
                            },
                            "rear-tire": {
                                "width": 205,
                                "aspect_ratio": 55,
                                "size": 16
                            }
                        }
                    ]
                }
        )
        self.assertEquals(response.status_code, 200)

    def test_user_tire_get_unauthorized_fail(self):

        user         = User.objects.get(id = 1)

        trim1 = Trim.objects.create(
            trim_id       = 1,
            front_tire_id = 1,
            back_tire_id  = 1,
        )
        trim2 = Trim.objects.create(
            trim_id       = 2,
            front_tire_id = 2,
            back_tire_id  = 2,
        )

        user.trim.add(trim1)
        user.trim.add(trim2)
        user.save()

        client = Client()
        headers = {"HTTP_Authorization" : '1'}
        response = client.get("/tires", **headers)

        self.assertEqual(
            response.json(),
            {'message': 'INVALID_TOKEN'}
        )
        self.assertEquals(response.status_code, 401)
