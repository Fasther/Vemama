from django.forms import ModelForm, HiddenInput
from tasks.models import Task


class CompleteTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["completed"].widget = HiddenInput()

    class Meta:
        model = Task
        fields = ("completed",)
