from django.db import models
from cars import models as cars
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=200)
    car = models.ForeignKey(cars.Car)
    user = models.ForeignKey(User)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True)
    completed_date = models.DateField(blank=True)

# TODO: str, done,