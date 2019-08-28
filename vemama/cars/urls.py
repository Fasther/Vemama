from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "cars"

urlpatterns = [
    path('', views.CityList.as_view(), name="city_list"),
    path("<int:city>/", views.CarsInCityList.as_view(), name="car_list"),
    path("<int:city>/<int:pk>", views.CarDetailView.as_view(), name="car_detail"),
    path("<int:city>/<int:pk>/edit", views.CarUpdateView.as_view(), name="car_edit"),
    path("<int:city>/<int:pk>/docheck", views.do_check, name="car_do_check"),
    path("<int:city>/<int:pk>/check", views.CarCheckView.as_view(), name="car_check"),
    path("test/", views.CarsInCityList.as_view(), name="test")
]

