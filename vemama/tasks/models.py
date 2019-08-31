from django.db import models
from cars import models as cars
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Task(models.Model):
    name = models.CharField(max_length=200)
    car = models.ForeignKey(cars.Car, related_name="tasks", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Person")
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    city = models.CharField(blank=True, null=True, max_length=150, verbose_name="City")
    completed = models.BooleanField(verbose_name="Completed", default=False)

    def save(self, *args, **kwargs):
        self.city = str(self.car.car_city)
        self.completed = True if self.completed_date else False
        if self.completed:
            self.is_past_due = "null"
        super().save(*args, **kwargs)

    def is_past_due(self):
        if not self.completed_date and self.due_date:
            try:
                return True if timezone.now().date() >= self.due_date else False
            except TypeError:
                pass
    is_past_due.boolean = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={'pk': self.pk})
