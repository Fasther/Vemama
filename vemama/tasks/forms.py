from django.forms import ModelForm
from tasks.models import Task


class CompleteTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("completed",)
