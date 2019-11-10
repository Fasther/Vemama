from django.contrib.auth import get_user_model
from tasks.models import Task

# this is used to assign users to tasks automatically

routine_check_name = "Routine check"  # routine check task name
inspection_name = "Regular service inspection soon"  # Regular service tasks name
fleet_grp = "fleet"  # surname for fleet group. Always used as: "{{ city }} fleet"
worker_gtp = "worker"  # surname for worker group. Always used as: "{{ city }} worker"


# Get tasks to be assigned

def get_tasks(tasks_name):
    tasks = Task.objects.filter(name=tasks_name, completed=False, user=None)
    tasks_dict = {}
    for task in tasks:
        tasks_dict.setdefault(task.city, []).append(task)
    return tasks_dict


# Get users in corresponding groups and they tasks counts

def assign_tasks(tasks: dict):
    task_type = " worker" if next(iter(tasks.items()))[1][0].name == "Routine check" else " fleet"
    for city in tasks:
        group_name = city + task_type
        users = get_user_model().objects.filter(groups__name=group_name)
        users_counts = {}  # get user counts to assign task to user with lowest tasks count
        for user in users:
            users_counts[user.username] = user.tasks.filter(completed=False).count()

# Assign the task to a person having the least number of tasks
