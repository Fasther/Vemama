from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView
from .models import City, Car
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = self.object.tasks.filter(completed=False).order_by("due_date")
        return context


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = "cars/car_form.html"
    fields = ["car_actual_driven_kms",
              "car_last_check",
              "car_tyres",
              "car_dirtiness",
              "car_next_inspection_date",
              "car_next_inspection_km",
              "car_next_oil_date",
              "car_next_oil_km",
              "car_next_stk_date",
              "car_note",
              ]


class CarCheckView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = "cars/car_check.html"
    fields = ["car_actual_driven_kms", "car_dirtiness", "car_note"]

    def form_valid(self, form):
        form.instance.car_last_check = timezone.now().date()
        return super().form_valid(form)
