import json
import bcrypt
import jwt
from json.decoder    import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from cardoc.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["id"]
            password = data["password"]

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message": "DUPLICATED_EMAIL"}, status = 400)

            encode_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            decode_password = encode_password.decode("utf-8")

            User.objects.create(
                email    = email,
                password = decode_password,
            )

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)

        return JsonResponse({"message" : "OK"}, status=200)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["id"]
            password = data["password"]

            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "LOGIN FAILED"}, status=401)

            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHM)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "LOGIN FAILED"}, status=401)

        return JsonResponse({"access_token": access_token}, status=200)
