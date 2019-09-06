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


def create_task(car, task_name):
    task = tasksmodels.Task(name=task_name, car=car, description="This task was created automatically")
    task.save()


def create_service_tasks():
    task_name = "Regular service inspection soon"  # service tasks name that will be used
    cars = carsmodels.Car.objects.all()
    tasks_created = 0
    for car in cars:
        car_needs_service = False
        # check for date - service in less than 30 days
        if timedelta(30) < (car.next_oil_or_inspection_date() - timezone.now().date()):
            car_needs_service = True
        # check for kms
        if car.next_oil_or_inspection_kms() < 3000:
            car_needs_service = True
        if car_needs_service:
            if not tasks_already_exist(car, task_name): # if task is not existing...
                create_task(car, task_name)
                tasks_created += 1
    return tasks_created

