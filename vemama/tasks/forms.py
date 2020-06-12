from django.forms import ModelForm, HiddenInput
from tasks.models import Task


class CompleteTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["completed_date"].widget = HiddenInput()

    class Meta:
        model = Task
        fields = ("completed_date",)


class CreateReportTask(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task_type"].choices = (
            (1, "Regular cleaning and check"),
            (99, "Other"),
        )

    class Meta:
        model = Task
        fields = ("name", "task_type", "description")
