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
              "car_next_inspection_date",
              "car_next_inspection_km",
              "car_next_oil_date",
              "car_next_oil_km",
              "car_note",
              ]


class CarCheckView(LoginRequiredMixin, DetailView):
    model = Car
    template_name = "cars/car_check.html"


@login_required
def do_check(request, pk, city):
    car = get_object_or_404(Car, pk=pk)
    car.do_check()
    return redirect('cars:car_detail', city=city, pk=pk)
