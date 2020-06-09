from cars.models import Car
from tasks.models import Task
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from tasks.models import Task


def task_already_exist(car, task_type):
    return car.tasks.filter(completed=False, task_type=task_type).exists()


def create_task(car, task_type, due_date):
    return Task.objects.create(car=car, task_type=task_type, due_date=due_date)

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
    cars = Car.objects.all()
    for car in cars:
        # check for car needs:
        if not car.needs_attention:
            continue
        else:
            if car.needs_cleaning:  # cleaning is subtype of check. So we want to plan it instead of check.
                task_type = Task.CLEANING
                time_from_last_check = timezone.now().date() - car.car_last_check
                if time_from_last_check > timedelta(days=settings.ROUTINE_CHECK_INTERVAL):
                    if not task_already_exist(car, task_type) and not task_already_exist(car, Task.CHECK):
                        due_date = timezone.now().date() + timedelta(days=settings.CHECK_TASK_DUE_DATE)
                        create_task(car, task_type, due_date)
            elif car.needs_check:
                task_type = Task.CHECK
                if not task_already_exist(car, task_type) and not task_already_exist(car, Task.CLEANING):
                    due_date = timezone.now().date() + timedelta(days=settings.CHECK_TASK_DUE_DATE)
                    create_task(car, task_type, due_date)

            if car.needs_service:
                task_type = Task.SERVICE
                if not task_already_exist(car, task_type):
                    due_date = (timezone.now().date() + settings.CAR_SERVICE_DAYS_THRESHOLD) if (
                            settings.CAR_SERVICE_KM_THRESHOLD > car.car_next_km) else car.car_next_date
                    create_task(car, task_type, due_date)
            if car.needs_stk:
                task_type = Task.STK
                current_month = timezone.now().strftime("%m")

                pass
            if car.needs_tyres_switch:
                task_type = Task.TYRES
                pass

    created_tasks = []
    return created_tasks
