from django.db import models
from cars import models as cars
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from tasks.notifications import send_notification
from simple_history.models import HistoricalRecords


class Task(models.Model):
    TASK_TYPES = (
        (1, "Regular cleaning and check"),
        (2, "Big cleaning and check"),
        (3, "Service check / Oil change"),
        (4, "STK"),
        (5, "Tyres change"),
        (99, "Other"),
    )
    name = models.CharField(max_length=200)
    car = models.ForeignKey(cars.Car, related_name="tasks", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name="Person")
    task_type = models.IntegerField(choices=TASK_TYPES, default=1)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    city = models.CharField(blank=True, null=True, max_length=150, verbose_name="City")
    completed = models.BooleanField(verbose_name="Completed", default=False)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.pk:  # notification for assigned user
            orig = Task.objects.get(pk=self.pk)
            if orig.user != self.user and (self.user is not None):
                send_notification("New task for you", [self, ])
        elif self.user:
            super().save(*args, **kwargs)
            send_notification("New task for you", [self, ])
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
        return reverse("tasks:task_detail",  kwargs={"last": "my", 'pk': self.pk})

    def complete(self):
        self.completed_date = timezone.now()
        self.save()
