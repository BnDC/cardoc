import requests
import re

from django.views import View

class CardocDataApi(View):
    def __init__(self):
        self.info_url = "https://dev.mycar.cardoc.co.kr/v1/trim/"

    def get_trim_information(self, trim_id):
        response = requests.get(self.info_url+str(trim_id), timeout = 3)

        return response
    
    def get_tire_information(self, response):
        data       = response.json()
        driving    = data["spec"]["driving"]
        front_tire = driving["frontTire"]
        back_tire  = driving["rearTire"]
        
        front_checker = re.match('^[\d]+/+[\d]+R+[\d]{1,}$', front_tire["value"])
        back_checker  = re.match('^[\d]+/+[\d]+R+[\d]{1,}$', back_tire["value"])

        if not (front_checker and back_checker):
            return None

        tires = (front_tire, back_tire)

        return tires

    def get_tire_value(self, tires):
        tire_value_list = [] 
        for tire in tires:
            value             = tire['value']
            value_string_list = re.findall("\d+", value)
            value_int_tuple   = tuple(map(int, value_string_list))

            tire_value_list.append(value_int_tuple)

        return tire_value_list