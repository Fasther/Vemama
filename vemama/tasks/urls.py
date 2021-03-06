from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="tasks_index"),
    path("active", views.ActiveTasksList.as_view(), name="active_tasks"),
    path("my", views.MyTasksList.as_view(), name="my_tasks"),
    path("overdue", views.OverdueTasksList.as_view(), name="overdue_tasks"),
    path("completed", views.CompletedTasksList.as_view(), name="completed_tasks"),
    path("unassigned", views.UnassignedTasksList.as_view(), name="unassigned_tasks"),
    path("<str:last>/<int:pk>", views.TaskDetail.as_view(), name="task_detail"),
    path("<str:last>/<int:pk>/edit", views.EditTask.as_view(), name="task_edit"),
    path("<str:last>/<int:pk>/do", views.DoTask.as_view(), name="do_task"),
    path("create", views.CreateTasksIndex.as_view(), name="create_tasks_index"),
    path("create/run", views.CreateTasks.as_view(), name="create_tasks"),
    path("create/notify-daily", views.send_daily_notification_view, name="send_daily_notify"),
    path("create/notify-weekly", views.send_weekly_notification_view, name="send_weekly_notify"),
    path("create/assign", views.AssignTasks.as_view(), name="assign_tasks"),

]
