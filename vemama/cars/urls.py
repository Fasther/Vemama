from django.urls import path
from . import views

app_name = "cars"

urlpatterns = [
    path('', views.CityList.as_view(), name="city_list"),
    path("<int:city>/", views.CarsInCityList.as_view(), name="car_list"),
    path("<int:city>/<int:pk>", views.CarDetailView.as_view(), name="car_detail"),
    path("<int:city>/<int:pk>/edit", views.CarUpdateView.as_view(), name="car_edit"),
    path("test/", views.CarsInCityList.as_view(), name="test")
]

