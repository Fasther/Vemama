from django import forms
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.db import models

from cars.models import City
from tasks.models import Task


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        res = super().to_python(value)
        if isinstance(res, list):
            value = [self.base_field.to_python(val) for val in res]
        return value


class Person(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Profile(models.Model):
    user = models.OneToOneField(Person, related_name="profile", on_delete=models.CASCADE, blank=False,
                                verbose_name="User")
    suitable_tasks = ChoiceArrayField(base_field=models.IntegerField(choices=Task.TASK_TYPES), blank=True)
    cities = models.ManyToManyField(City, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
