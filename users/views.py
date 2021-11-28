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
            email    = data['email']
            password = data['password']

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message": "DUPLICATED_EMAIL"}, status=400)

            encode_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decode_password = encode_password.decode('utf-8')

            User.objects.create(
                email    = email,
                password = decode_password,
            )

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)