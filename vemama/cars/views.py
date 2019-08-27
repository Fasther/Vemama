from django.views.generic import ListView, DetailView
from .models import City, Car
from django.contrib.auth.mixins import LoginRequiredMixin


class CityList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = City
    template_name = "cars/city_list.html"
    context_object_name = "cities"


class CarsInCityList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = Car
    template_name = "cars/cars_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        return Car.objects.filter(car_city__exact=self.kwargs["city"])


class CarDetailView(LoginRequiredMixin, DetailView):
    model = Car
    template_name = "cars/car_detail.html"
