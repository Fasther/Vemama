from django.forms import model_to_dict
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from pylint.checkers import initialize

from cars.forms import CarTaskForm
from .forms import CompleteTaskForm
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from tasks import create_tasks, notifications, assign_tasks


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
        return Task.objects.filter(completed=True, completed_date__gte=(timezone.now()-timedelta(days=60)))

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


class CreateTasks(LoginRequiredMixin, TemplateView):
    template_name = "tasks/create_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:  # show message of what work have been done (created tasks, send emails,...)
            context["msg"] = self.request.session.pop("msg")
        except KeyError:
            pass
        return context


class DoTask(LoginRequiredMixin, TemplateView):
    template_name = "tasks/tasks_do.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_instance = get_object_or_404(Task, pk=kwargs.get("pk"))
        task_type = task_instance.task_type
        car_instance = task_instance.car
        context["car"] = car_instance
        context["task"] = task_instance

        if task_type == Task.CHECK:
            exclude = ("car_tyres",)

        context["car_form"] = CarTaskForm(exclude_fields=("car_actual_driven_kms",),
                                          instance=car_instance,
                                          )
        context["task_form"] = CompleteTaskForm(initial={"completed": True, }, instance=task_instance)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@login_required
def mark_as_complete(request, pk, last):
    task = get_object_or_404(Task, pk=pk)
    if task.name == "Routine check":
        task.car.do_check()
    task.complete()
    return redirect('tasks:task_detail', last=last, pk=pk)


def create_service_tasks_view(request):
    msg = create_tasks.create_service_tasks()
    request.session['msg'] = "I have created {} new service tasks".format(msg)
    return redirect("tasks:create_tasks")


def create_check_tasks_view(request):
    msg = create_tasks.create_check_tasks()
    request.session['msg'] = "I have created {} new check tasks".format(msg)
    return redirect("tasks:create_tasks")


def send_daily_notification_view(request):
    msg = notifications.summary_notification("Tasks due tomorrow", 1)
    request.session['msg'] = "I have sent {} email(s) about tasks due tomorrow".format(msg)
    return redirect("tasks:create_tasks")


def send_weekly_notification_view(request):
    msg = notifications.summary_notification("Tasks due this week", 7)
    request.session['msg'] = "I have sent {} email(s) about tasks due in this week".format(msg)
    return redirect("tasks:create_tasks")


def assign_tasks_view(request):
    msg = assign_tasks.assign_check_inspection_tasks()
    request.session['msg'] = "I have assigned {} tasks".format(msg)
    return redirect("tasks:create_tasks")
