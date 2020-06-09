from cars.models import Car
from tasks.models import Task
from datetime import timedelta, datetime, date
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
    created_tasks = []
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
                        created_tasks.append(create_task(car, task_type, due_date))
            elif car.needs_check:
                task_type = Task.CHECK
                if not task_already_exist(car, task_type) and not task_already_exist(car, Task.CLEANING):
                    due_date = timezone.now().date() + timedelta(days=settings.CHECK_TASK_DUE_DATE)
                    created_tasks.append(create_task(car, task_type, due_date))

            if car.needs_service:
                task_type = Task.SERVICE
                if not task_already_exist(car, task_type):
                    due_date = (timezone.now().date() + settings.CAR_SERVICE_DAYS_THRESHOLD) if (
                            settings.CAR_SERVICE_KM_THRESHOLD > car.car_next_km) else car.car_next_date
                    created_tasks.append(create_task(car, task_type, due_date))
            if car.needs_stk:
                task_type = Task.STK
                if not task_already_exist(car, task_type):
                    created_tasks.append(create_task(car, task_type, car.car_next_stk_date))
            if car.needs_tyres_switch:
                task_type = Task.TYRES
                if not task_already_exist(car, task_type):
                    current_month = int(timezone.now().strftime("%m"))
                    if current_month in (9, 10, 11):
                        month, day = settings.WINTER_TYRE_SWITCH_DUE_DATE
                    elif current_month in (3, 4, 5):
                        month, day = settings.SUMMER_TYRE_SWITCH_DUE_DATE
                    else:
                        month, day = (timezone.now() +
                                      timedelta(days=settings.CAR_SERVICE_DAYS_THRESHOLD)).strftime("%m,%d").split(",")
                    due_date = date(timezone.now().year, int(month), int(day))
                    created_tasks.append(create_task(car, task_type, due_date))
    return created_tasks
