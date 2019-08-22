from django.db import models
from cars import models as cars
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=200)
    car = models.ForeignKey(cars.Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name