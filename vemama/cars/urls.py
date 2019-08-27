from django.urls import path
from . import views

app_name = "cars"

urlpatterns = [
    path('', views.CityList.as_view(), name="city_list"),
]