import jwt

from django.http     import JsonResponse

from users.models    import User
from cardoc.settings import SECRET_KEY, ALGORITHM

def login_required(func) :
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers: 
            return JsonResponse ({'message' : 'UNAUTHORIZED'}, status = 401)

        try :
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = payload['id'])
            request.user = user

        except User.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except jwt.exceptions.DecodeError :
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper
