import jwt
import bcrypt
import json

from django.test  import TestCase, Client

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class Test(TestCase):
    def setUp(self):
        self.password = bcrypt.hashpw("abc1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        User.objects.bulk_create([
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
                email    = "user3@gmail.com",
                password = self.password
            ),
        ])

        self.access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm=ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
    
    def test_post_success_signup(self):
        client = Client()
        data   = {
            "email"    : "test1@naver.com",
            "password" : "abc1234",
        }
        response = client.post("/users/signup", json.dumps(data), content_type="applications/json")

        self.assertEqual(response.json(),
            {
                "message": "CREATED"
            }
        )
        self.assertEquals(response.status_code, 201)
    
    def test_post_fail_signup_keyerror(self):
        client   = Client()
        data     = {}
        response = client.post("/users/signup", json.dumps(data), content_type = "applications/json")

        self.assertEqual(response.json(),
            {
                "message": "KEY_ERROR"
            }
        )
        self.assertEquals(response.status_code, 400)
    
    def test_post_fail_signup_duplicated_email(self):
        client = Client()
        data   = {
            "email"    : "user1@naver.com",
            "password" : "abc1234",
        }
        response = client.post('/users/signup', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "DUPLICATED_EMAIL"
            }
        )
        self.assertEquals(response.status_code, 400)

    def test_post_success_signin(self):
        client = Client()
        data   = {
            "email"    : "user2@naver.com",
            "password" : "abc1234"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')
        user     = User.objects.get(email = data['email'])

        self.assertEqual(response.json(),
            {
                "access_token": self.access_token
            }
        )
        self.assertEquals(response.status_code, 200)
    
    def test_post_fail_signin_do_not_exist_user(self):
        client = Client()
        data   = {
            "email"    : "user999@naver.com",
            "password" : "abc1234"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "LOGIN FAILED"
            }
        )
        self.assertEquals(response.status_code, 401)
    
    def test_post_fail_signin_input_wrong_password(self):
        client = Client()
        data   = {
            "email"    : "user2@naver.com",
            "password" : "00000"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')
        
        if not bcrypt.checkpw(data["password"].encode('utf-8'), self.password.encode('utf-8')):
        
            self.assertEqual(response.json(),
                {
                    "message": "LOGIN FAILED"
                }
            )
            self.assertEquals(response.status_code, 401)
    
    def test_post_fail_signin_keyerror(self):
        client   = Client()
        data     = {}
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "KEY_ERROR"
            }
        )
        self.assertEquals(response.status_code, 400)
