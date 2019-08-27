from django.views.generic import ListView
from .models import City, Car
from django.contrib.auth.mixins import LoginRequiredMixin


class CityList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = City
    template_name = "cars/city-list.html"
    context_object_name = "cities"

