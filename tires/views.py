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


'''
            return JsonResponse({'before_balance' : before_balance, 'after_balance' : last_balance}, status=201)
        
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
        
        except Account.DoesNotExist:
            return JsonResponse({'message' : 'ACCOUNT_DOES_NOT_EXIST'}, status = 404)
        
        except DealPosition.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_DEAL_POSITION_ID'}, status = 400)
        
        except ValidationError as e:
            return JsonResponse({'message' : (e.message)}, status = 400)
    
    #거래내역 조회
    #@login_decorator
    def get(self, request, account_id):
        try:
            CheckError.check_account_id(account_id)
            
            account = Account.objects.get(id = account_id)
            user    = request.user

            if not account.owner_id == user.id:
                return JsonResponse({'message' : 'INVALID_ACCOUNT_ID'}, status = 400)

            start_date       = request.GET['start_date']
            end_date         = request.GET['end_date']
            sort             = request.GET.get('sort')
            deal_position_id = request.GET.get('deal_position_id')
            page             = int(request.GET.get('page', 1))

            page_size = 500
            limit     = page_size * page
            offset    = limit - page_size

            sort_by = {
                'recent' : '-created_at',
                'old'    : 'created_at'
            }
            
            deal_filter = (Q(created_at__date__range = (start_date, end_date)) & Q(account_id = account_id))

            if deal_position_id:
                CheckError.check_deal_position_id(deal_position_id)
                
                deal_filter.add(Q(deal_position_id = deal_position_id), Q.AND)

            deals = Deal.objects.select_related('deal_position').filter(deal_filter).order_by(sort_by.get(sort, '-created_at'))[offset : limit]

            data = [{
                'id'            : deal.id,
                'deal_position' : deal.deal_position.position,
                'deal_date'     : deal.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deal_amount'   : deal.amount,
                'deal_balance'  : deal.balance,
                'description'   : deal.description,
                } for deal in deals]

            return JsonResponse({'data' : data}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except ValidationError:
            return JsonResponse({'message' : 'INVALID_DATE'}, status = 400)
        
        except Account.DoesNotExist:
            return JsonResponse({'message' : 'ACCOUNT_DOES_NOT_EXIST'}, status = 404)
        
        except DealPosition.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_DEAL_POSITION_ID'}, status = 400)
'''