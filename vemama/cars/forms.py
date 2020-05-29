from django.forms import ModelForm, HiddenInput
from cars.models import Car


class CarTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)
        super().__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields[field].widget = HiddenInput()

    class Meta:
        model = Car
        fields = ["car_actual_driven_kms", "car_dirtiness", "car_tyres", "car_note"]
        exclude = []
