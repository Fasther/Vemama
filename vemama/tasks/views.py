from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from rest_framework.views import APIView
from rest_framework import authentication

from cars.forms import CarTaskForm
from cars.models import Car
from tasks import notifications
from .assign_tasks import assign_all_tasks
from .create_tasks import create_all_tasks
from .forms import CompleteTaskForm
from .models import Task


class TasksIndexView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/tasks_index.html"


class ActiveTasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(completed_date__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual_page"] = "Active tasks"
        context["last"] = "active"
        return context


class MyTasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, completed=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual_page"] = "My tasks"
        context["last"] = "my"
        return context


class UnassignedTasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual_page"] = "Unassigned tasks"
        context["last"] = "unassigned"
        return context


class OverdueTasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(completed=False, due_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual_page"] = "Overdue tasks"
        context["last"] = "overdue"
        return context


class CompletedTasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(completed=True, completed_date__gte=(timezone.now() - timedelta(days=60)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual_page"] = "Completed tasks"
        context["last"] = "completed"
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = "tasks/tasks_detail.html"
    model = Task


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "tasks/tasks_form.html"
    fields = [
        "name",
        "description",
        "due_date",
        "completed_date",
    ]

    def get_success_url(self):
        last = self.kwargs.get("last")
        pk = self.kwargs.get("pk")
        return reverse("tasks:task_detail", kwargs={"last": last, "pk": pk})


class CreateTasksIndex(LoginRequiredMixin, TemplateView):
    template_name = "tasks/create_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:  # show message of what work have been done (created tasks, send emails,...)
            context["msg"] = self.request.session.pop("msg")
        except KeyError:
            pass
        return context


class CreateTasks(APIView):
    authentication_classes = (authentication.BasicAuthentication,)

    def get(self, request, *args, **kwargs):
        created_tasks = create_all_tasks()

        enumerated_tasks = []
        for order, task in enumerate(created_tasks):
            enumerated_tasks.append(f"{order:>2}: {task}")
        enumerated_tasks = "\n".join(enumerated_tasks)

        return HttpResponse(f"-- Create tasks {timezone.now().strftime('%X %x')} -----\n"
                            f"Created: {len(created_tasks)}\n"
                            f"List of tasks:\n"
                            f"{enumerated_tasks}\n"
                            f"{36 * '-'}\n",
                            content_type="text/plain")


class AssignTasks(APIView):
    authentication_classes = (authentication.BasicAuthentication,)

    def get(self, request, *args, **kwargs):
        assigned_tasks = assign_all_tasks()

        enumerated_tasks = []
        for order, task in enumerate(assigned_tasks):
            enumerated_tasks.append(f"{order:>2}: {task}")
        enumerated_tasks = "\n".join(enumerated_tasks)

        return HttpResponse(f"-- Assign tasks {timezone.now().strftime('%X %x')} -----\n"
                            f"Assigned: {len(assigned_tasks)}\n"
                            f"List of tasks:\n"
                            f"{enumerated_tasks}\n"
                            f"{36 * '-'}\n",
                            content_type="text/plain")


class DoTask(LoginRequiredMixin, TemplateView):
    template_name = "tasks/tasks_do.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_instance = get_object_or_404(Task, pk=kwargs.get("pk"))
        task_type = task_instance.task_type
        car_instance = task_instance.car
        context["car"] = car_instance
        context["task"] = task_instance

        car_check_actions = (
            "Car checks:\n"
            "- I checked oil level\n- I checked tire pressures\n- I topped up the washer fluid\n"
            "- I checked all lights are functional",

            "Equipment checks:\n"
            "- Safety vest at drivers door\n- First aid kit\n- Warning triangle\n"
            "- Chains and scrapers (in winter-time)\n- Charger and holder - all functional\n",

            "Log book checks:\n"
            "- I picked up all bills from log-book and placed them to separate folder.\n"
            "- There are all legal documents for car (ORV, Insurance card, CCS card, European Accident statement)\n"
            "- Papers with: Info about car, Map with zone, expenses not payed by CCS card, damage report"
        )

        if task_type == Task.CHECK:
            exclude = ("car_tyres", "car_next_oil_date", "car_next_oil_km", "car_next_inspection_date",
                       "car_next_inspection_km", "car_next_stk_date",)
            context["task_info"] = "This is regular maintenance task. Do checks.\n" \
                                   "Please follow instructions and edit car info, if needed."
            context["task_actions"] = (
                                          "Cleaning:\n"
                                          "- The car is washed and clean\n- I vacuumed seats and floor\n- I cleaned "
                                          "all plastic parts\n- I disinfected the steering wheel and other surfaces "
                                          "that are often touched.\n- Windows are clean\n",
                                      ) + car_check_actions
        elif task_type == Task.CLEANING:
            exclude = ("car_dirtiness", "car_tyres", "car_next_oil_date", "car_next_oil_km", "car_next_inspection_date",
                       "car_next_inspection_km", "car_next_stk_date",)
            context["task_info"] = "Car needs bigger cleaning, also with wet cleaning of seats.\n" \
                                   "Also do regular check."
            context["task_actions"] = (
                "Wet cleaning:\n"
                "- Plan appointment for this car at local cleaning business.\n"
                "- Take the car to cleaning\n"
                "- and from cleaning :)"
            )
        elif task_type == Task.SERVICE:
            exclude = ("car_tyres", "car_next_stk_date",)
            context["task_info"] = "Car needs service soon!\n" \
                                   f"KMs till service: {car_instance.car_next_km}, " \
                                   f"Service date: {date_format(car_instance.car_next_date, 'DATE_FORMAT')}\n" \
                                   f"Please plan service appointment for {car_instance.car_name} in your local car " \
                                   "service"
            context["task_actions"] = ("Plan appointment, reserve car for that date.", "Take car to the service",
                                       "Take it back", "Update service info")
        elif task_type == Task.STK:
            exclude = ("car_tyres", "car_next_oil_date", "car_next_oil_km", "car_next_inspection_date",
                       "car_next_inspection_km", "car_dirtiness",)
            context["task_info"] = f"{car_instance.car_name} will need STK check.\n " \
                                   f"STK is valid till: " \
                                   f"{date_format(car_instance.car_next_stk_date, 'DATE_FORMAT') if car_instance.car_next_stk_date else 'Unknown'}"
            context["task_actions"] = ('Get "Velký TP" from Brno Office',
                                       "If needed, make appointment at local STK workshop",
                                       "Check, that car looks ok (lights, etc). If not, fix it.",
                                       "Take the car to STK workshop and do STK inspection",
                                       "Update next STK date.")

        elif task_type == Task.TYRES:
            exclude = ("car_next_oil_date", "car_next_oil_km", "car_next_inspection_date", "car_next_inspection_km",
                       "car_next_stk_date",)
            context["task_info"] = "Car needs check, if tyres are still good!" if \
                car_instance.car_tyres == Car.TYRE_ALL_YEAR else "Car needs seasonal tyre change!"
            all_year_action = ("Check if car have at least 4.5mm tread depth on all tyres.",
                               "If yes, check that the front ones are not significantly shallower than the rear ones.\n"
                               "- If yes, plan tyre rotation\n- If not, your task is done.",
                               "If no, order new ones and do regular tyre change (see bellow):",) \
                if car_instance.car_tyres == Car.TYRE_ALL_YEAR else ()
            context["task_actions"] = all_year_action + (
                "Check, that you have right tyres for replacement.\n"
                "- if not, order them.",
                "Plan appointment in your local service for tyre change",
                "Take the car for tyre change", "Write current tyres bellow and this task is done",
            )
        else:  # task_type == OTHER
            exclude = ("car_tyres", "car_next_oil_date", "car_next_oil_km", "car_next_inspection_date",
                       "car_next_inspection_km", "car_next_stk_date",)
            context["task_info"] = "Special task! See description bellow. \n"
            context["task_actions"] = (f"Description:\n{task_instance.description}",)

        context["car_form"] = CarTaskForm(exclude_fields=exclude,
                                          instance=car_instance,
                                          )
        context["task_form"] = CompleteTaskForm(initial={"completed_date": timezone.now().date(), },
                                                instance=task_instance)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        task_instance = get_object_or_404(Task, pk=kwargs.get("pk"))
        car_instance = task_instance.car
        car_form = CarTaskForm(self.request.POST, instance=car_instance)
        task_form = CompleteTaskForm(self.request.POST, instance=task_instance)
        if car_form.is_valid() and task_form.is_valid():
            car = car_form.save(commit=False)
            if task_instance.task_type == Task.CHECK:
                car.car_last_check = timezone.now().date()
            elif task_instance.task_type == Task.CLEANING:
                car.car_dirtiness = 1  # clean car
                car.car_last_check = timezone.now().date()
            car.save()
            task_form.save()

            return HttpResponseRedirect(reverse("tasks:task_detail", kwargs={**kwargs}))

        else:
            kwargs["errors"] = car_form.errors
            return self.get(request, *args, **kwargs)

# TODO rework notifications

@login_required
def send_daily_notification_view(request):
    msg = notifications.summary_notification(f" Tasks due tomorrow ({timezone.now().strftime('%d/%m')})", 1)
    request.session['msg'] = "I have sent {} email(s) about tasks due tomorrow".format(msg)
    return redirect("tasks:create_tasks_index")


@login_required
def send_weekly_notification_view(request):
    msg = notifications.summary_notification(" Tasks due upcoming week", 7)
    request.session['msg'] = "I have sent {} email(s) about tasks due in this week".format(msg)
    return redirect("tasks:create_tasks_index")
