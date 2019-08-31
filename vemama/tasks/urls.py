from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "tasks"

urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="tasks_index"),
    path("all", views.AllActiveTasksList.as_view(), name="all_tasks"),
    path("my", views.MyTasksList.as_view(), name="my_tasks"),
    path("<str:last>/<int:pk>", views.TaskDetail.as_view(), name="task_detail"),
]
