from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from rest_framework import authentication
from rest_framework.views import APIView

from tasks.assign_tasks import assign_task
from tasks.forms import CreateReportTask
from cars.models import City, Car


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
        try:  # show message of what work have been done
            context["car_msg"] = self.request.session.pop("car_msg")
        except KeyError:
            pass
        return context


class CarReport(LoginRequiredMixin, TemplateView):
    template_name = "cars/car_report.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        car = get_object_or_404(Car, pk=kwargs.get("pk"))
        context["car"] = car
        context["task_form"] = CreateReportTask(initial={"description": "Manually reported problem"})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=kwargs.get("pk"))
        task_form = CreateReportTask(self.request.POST)
        if task_form.is_valid():

            task_instance = task_form.save(commit=False)
            task_instance.car = car
            task_instance.due_date = timezone.now().date() + timedelta(days=settings.CHECK_TASK_DUE_DATE)
            task_instance.save()
            task_instance = assign_task(task_instance)
            request.session["car_msg"] = f'Task "{task_instance}" created. Assigned to {task_instance.user}.'
            return HttpResponseRedirect(reverse("cars:car_detail", kwargs={**kwargs}))
        else:
            kwargs["errors"] = task_form.errors
            return self.get(request, *args, **kwargs)


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

    def post(self, request, *args, **kwargs):
        request.session["car_msg"] = "Car updated successfully!"
        return super().post(self, request, *args, **kwargs)


class CarCheckView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = "cars/car_check.html"
    fields = ["car_actual_driven_kms", "car_dirtiness", "car_note"]

    def form_valid(self, form):
        form.instance.car_last_check = timezone.now().date()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        request.session["car_msg"] = "Check completed! Thank you!"
        return super().post(self, request, *args, **kwargs)


class UpdateActualDrivenKMsFromZemtu(APIView):
    authentication_classes = (authentication.BasicAuthentication,)

    def __init__(self):
        super().__init__()
        self.zemtu_url = "https://autonapul.zemtu.com/api/v2/reservationaccounting/?&state=closed&reservation_end__gte="
        self.token = settings.Z_TOKEN

    @staticmethod
    def update_driven_kms(car_id, driven_kms):
        try:
            car_instance = Car.objects.get(car_id=car_id)
            car_instance.car_actual_driven_kms = int(driven_kms)
            car_instance.save()
            return car_instance
        except (Car.DoesNotExist, TypeError):
            return None

    def get_driven_kms(self, parsed_json_data: dict):
        updated_cars = []
        for result in parsed_json_data.get("results"):
            try:
                updated_car = self.update_driven_kms(
                    result['vehicle']['id'], result['odometer_end']
                )
                if updated_car:
                    updated_cars.append(updated_car)
                else:
                    continue
            except KeyError:
                pass

        return updated_cars

    def get(self, request, *args, **kwargs):
        from_date = timezone.now().date() - timedelta(days=1)
        iso_time = from_date.strftime("%Y-%m-%dT00:00:00Z")
        headers = {"Authorization": f"Token {self.token}"}
        zemtu_data = requests.get(self.zemtu_url + iso_time, headers=headers)
        if zemtu_data.ok:
            updated_cars = self.get_driven_kms(zemtu_data.json())
            enum_updates = []
            for order, car in enumerate(updated_cars):
                enum_updates.append(f"{order:>3}: {car} ({car.car_actual_driven_kms} km)")
            enum_updates = "\n".join(enum_updates)
            return HttpResponse(f"-- KMs update -- {timezone.now().strftime('%X %x')}\n"
                                f"Updated: {len(updated_cars)}\n"
                                f"List of cars:\n"
                                f"{enum_updates}", content_type="text/plain", status=200)
        else:
            return HttpResponse(f"-- KMs update -- {timezone.now().strftime('%X %x')}\n"
                                f"Response not OK:\n"
                                f"{zemtu_data.status_code}: {zemtu_data.reason}",
                                content_type="text/plain", status=400)
