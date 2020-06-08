from cars import models as carsmodels
from tasks import models as tasksmodels
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from tasks.models import Task


def tasks_already_exist(car, task_name):
    tasks = car.tasks.filter(completed=False)
    for task in tasks:
        if task.name == task_name:
            return True
    return False


def create_task(car, task_name, due_date):
    task = tasksmodels.Task(name=task_name,
                            car=car,
                            description="This task was created automatically",
                            due_date=due_date)
    task.save()


def create_service_tasks():
    task_name = "Regular service inspection soon"  # service tasks name that will be used
    cars = carsmodels.Car.objects.all()
    tasks_created = 0
    due_date = timezone.now().date() + timedelta(30)
    for car in cars:
        car_needs_service = False
        # check for date - service in less than 30 days
        if timedelta(30) > (car.next_oil_or_inspection_date() - timezone.now().date()):
            car_needs_service = True
        # check for kms
        # TODO this needs change!
        if car.next_oil_or_inspection_kms() < 3000:
            car_needs_service = True
        if car_needs_service:
            if not tasks_already_exist(car, task_name):  # if task is not existing...
                create_task(car, task_name, due_date)
                tasks_created += 1
    return tasks_created


def create_check_tasks():
    task_name = "Routine check"
    cars = carsmodels.Car.objects.all()
    tasks_created = 0
    due_date = timezone.now().date() + timedelta(15)
    for car in cars:
        if timedelta(days=settings.ROUTINE_CHECK_INTERVAL) < (timezone.now().date() - car.car_last_check):
            if not tasks_already_exist(car, task_name):
                create_task(car, task_name, due_date)
                tasks_created += 1
    return tasks_created


def create_all_tasks():
    cars = carsmodels.Car.objects.all()
    for car in cars:
        # check for car needs:
        if not car.needs_attention:
            continue
        else:
            if car.needs_check:
                task_type = Task.CHECK
                # check if tasks not exist
                # create one
                pass
            if car.needs_cleaning:
                task_type = Task.CLEANING
                pass
            if car.needs_service:
                task_type = Task.SERVICE
                pass
            if car.needs_stk:
                task_type = Task.STK
                pass
            if car.needs_tyres_switch:
                task_type = Task.TYRES
                pass

    created_tasks = []
    return created_tasks
