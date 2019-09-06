from cars import models as carsmodels
from tasks import models as tasksmodels
from datetime import timedelta
from django.utils import timezone


def create_check_tasks():
    cars = carsmodels.Car.objects.all()
    for car in cars:
        car_needs_service = False
        # check for date - service in less than 30 days
        if timedelta(30) > (car.next_oil_or_inspection_date() - timezone.now().date()):
            car_needs_service = True
        # check for kms
        if car.next_oil_or_inspection_kms() < 3000:
            car_needs_service = True



