from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "tasks"

urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="tasks_index"),
    path("active", views.ActiveTasksList.as_view(), name="active_tasks"),
    path("my", views.MyTasksList.as_view(), name="my_tasks"),
    path("<str:last>/<int:pk>", views.TaskDetail.as_view(), name="task_detail"),
]