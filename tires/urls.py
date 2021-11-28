from django.urls import path

from tires.views import TireView


urlpatterns = [
    path("", TireView.as_view()),
]