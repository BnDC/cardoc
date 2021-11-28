import json

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from users.models import User
from users.utils  import login_required
from tires.models import Trim, Tire
from tires.utils  import CardocDataApi

class TireView(View):
    def post(self, request):
        cardoc = CardocDataApi()

        try:
            data = json.loads(request.body)

            if not data:
                return JsonResponse({"message": "EMPTY_BODY"}, status = 400)

            if len(data) > 5:
                return JsonResponse({"message" : "TOO_MUCH_REQUEST"}, status = 400)
            
            with transaction.atomic():
                for datum in data:
                    trim_id  = datum['trimId']
                    response = cardoc.get_trim_information(trim_id)
                    email    = datum["id"]
                    
                    user = User.objects.get(email = email)
                    
                    if response.status_code != 200:
                        return JsonResponse({"message " : "INVALID_TRIM_ID"}, status = 400)

                    tires = cardoc.get_tire_information(response)

                    if not tires:
                        return JsonResponse({"message" : "INVALID_TIRE_FORM"}, status = 400)

                    values = cardoc.get_tire_value(tires)

                    for index, value in enumerate(values):
                        width        = value[0]
                        aspect_ratio = value[1]
                        size         = value[2]

                        if index == 0:
                            front_tire, _ = Tire.objects.get_or_create(
                                width        = width,
                                aspect_ratio = aspect_ratio,
                                size         = size,
                            )

                        else:
                            back_tire, _ = Tire.objects.get_or_create(
                                width        = width,
                                aspect_ratio = aspect_ratio,
                                size         = size,
                            )

                    trim, _ = Trim.objects.get_or_create(
                        trim_id    = trim_id,
                        front_tire = front_tire,
                        back_tire  = back_tire
                    )

                    user.trim.add(trim)

            return JsonResponse({"message": "OK"}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_NOT_EXIST"}, status = 400)

    @login_required
    def get(self, request):
        user = request.user
        print(user.id)
        trims = user.trim.all().prefetch_related('front_tire','back_tire')

        tires = [{
            "trim_id": trim.trim_id,
            "front-tire" : {
                "width"        : trim.front_tire.width,
                "aspect_ratio" : trim.front_tire.aspect_ratio,
                "size"         : trim.front_tire.size,
            },
            "rear-tire" : { 
                "width"        : trim.back_tire.width,
                "aspect_ratio" : trim.back_tire.aspect_ratio,
                "size"         : trim.back_tire.size,
            },
            } for trim in trims]

        return JsonResponse({"result" : tires}, status = 200)