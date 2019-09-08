from cars import models as carsmodels
from tasks import models as tasksmodels
from datetime import timedelta
from django.utils import timezone


def tasks_already_exist(car, task_name):
    tasks = car.tasks.all()
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
        if timedelta(30) < (car.next_oil_or_inspection_date() - timezone.now().date()):
            car_needs_service = True
        # check for kms
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
        if timedelta(30) < (timezone.now().date() - car.car_last_check):
            if not tasks_already_exist(car, task_name):
                create_task(car, task_name, due_date)
                tasks_created += 1
    return tasks_created
