from django.contrib.auth import get_user_model
from django.db.models import Q, Count

from core.models import Profile
from tasks.models import Task


# # this is used to assign users to tasks automatically
#
# # TODO This needs serious work over.
#
# routine_check_name = "Routine check"  # routine check task name
# inspection_name = "Regular service inspection soon"  # Regular service tasks name
# fleet_grp = "fleet"  # surname for fleet group. Always used as: "{{ city }} fleet"
# worker_gtp = "worker"  # surname for worker group. Always used as: "{{ city }} worker"
#
#
# # Get tasks to be assigned and group them by city
#
# def get_tasks(tasks_name):
#     tasks = Task.objects.filter(name=tasks_name, completed=False, user=None)
#     tasks_dict = {}
#     for task in tasks:
#         tasks_dict.setdefault(task.city, []).append(task)
#     return tasks_dict
#
#
# # Assign tasks based on city
#
# def assign_tasks(tasks: dict):
#     if not tasks:
#         return 0
#     task_type = " fleet" if next(iter(tasks.items()))[1][0].name == inspection_name else " worker"
#     tasks_assigned = 0
#     for city in tasks:
#         group_name = city + task_type
#         users = get_user_model().objects.filter(groups__name=group_name)
#         users_counts = {}  # get user counts to assign task to user with lowest tasks count
#         for user in users:
#             users_counts[user] = user.tasks.filter(completed=False).count()
#         for task in tasks[city]:
#             user = min(users_counts, key=users_counts.get)
#             task.user = user
#             task.save()
#             users_counts[user] += 1
#             tasks_assigned += 1
#     return tasks_assigned
#
#
# def assign_check_inspection_tasks():  # main function returning results to view
#     assigned_tasks_count = assign_tasks(get_tasks(routine_check_name)) + \
#                            assign_tasks(get_tasks(inspection_name))
#     return assigned_tasks_count

def assign_task(task: Task):
    from tasks.models import Task
    task = Task.objects.get(id=281)
    suitable_workers = Profile.objects.filter(
        user__is_active=True, cities__name__contains=task.city, suitable_tasks__contains=[task.task_type]
    )
    if not suitable_workers:
        suitable_workers = Profile.objects.filter(user__is_superuser=True)
        task.description = f'Task assigned to SuperUser because no Person available in "{task.city}" ' \
                           f'to do "{task.get_task_type_display()}".'
    suitable_worker = suitable_workers.annotate(
        tasks=Count("user__tasks", filter=Q(user__tasks__completed=False))).order_by("-tasks").first()

    # filter workers by city
    # filter by task type, if None assing to staff
    # if still none, assign to super_user by lowest ID
    return task


def assign_all_tasks():
    unassigned_tasks = Task.objects.filter(completed=False, user=None)
    assigned_tasks = []
    for task in unassigned_tasks:
        assigned_tasks.append(assign_task(task))
    return assigned_tasks
