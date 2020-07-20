from django.db.models import Q, Count

from core.models import Profile
from tasks.models import Task


def assign_task(task: Task):
    suitable_workers = Profile.objects.filter(
        user__is_active=True, cities__name__contains=task.city, suitable_tasks__contains=[task.task_type]
    )
    if not suitable_workers:
        suitable_workers = Profile.objects.filter(user__is_superuser=True)
        task.description = f'Task assigned to SuperUser because no Person available in "{task.city}" ' \
                           f'to do "{task.get_task_type_display()}".'
    suitable_worker = suitable_workers.annotate(
        tasks=Count("user__tasks", filter=Q(user__tasks__completed=False))).order_by("tasks").first()
    task.user = suitable_worker.user
    task.save()
    return task


def assign_all_tasks():
    unassigned_tasks = Task.objects.filter(completed=False, user=None)
    assigned_tasks = []
    for task in unassigned_tasks:
        assigned_tasks.append(assign_task(task))
    return assigned_tasks
