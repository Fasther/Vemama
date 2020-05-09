from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django import forms
from tasks.models import Task
from cars.models import City


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


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="profile", on_delete=models.CASCADE, blank=False,
                                verbose_name="User")
    suitable_tasks = ChoiceArrayField(base_field=models.IntegerField(choices=Task.TASK_TYPES))
    cities = models.ManyToManyField(City)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
