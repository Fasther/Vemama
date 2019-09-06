from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


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
        return Task.objects.filter(due_date__lte=timezone.now())

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


@login_required
def mark_as_complete(request, pk, last):
    task = get_object_or_404(Task, pk=pk)
    task.complete()
    return redirect('tasks:task_detail', last=last, pk=pk)