from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cars:car_list", kwargs={'city': self.pk})

    class Meta:
        verbose_name_plural = "Cities"


class Car(models.Model):
    CAR_TYRES = (
        (1, "All year"),
        (2, "Summer"),
        (3, "Winter")
    )
    DIRTINESS = (
        (1, "Fine, looks good"),
        (2, "Few stains, still good enough"),
        (3, "Car needs wet cleaning. Really.")
    )
    is_active = models.BooleanField(default=True, verbose_name="Active",
                                    help_text="Use to deactivate car. Deactivated cars "
                                              "do not get automatic tasks and reminders.")
    car_name = models.CharField(max_length=200, unique=True, verbose_name="Name")
    car_id = models.DecimalField(unique=True, decimal_places=0, max_digits=5, verbose_name="External ID",
                                 help_text="ID for finding car in Zemtu, Convadis,...")
    car_city = models.ForeignKey(City, related_name="cars", on_delete=models.CASCADE, verbose_name="City")
    car_tyres = models.IntegerField(choices=CAR_TYRES, blank=True, null=True, default=1, verbose_name="Actual Tyres",
                                    help_text="If seasonal tyre change is needed, task will be planned")
    car_dirtiness = models.IntegerField(choices=DIRTINESS, blank=True, null=True, default=1,
                                        verbose_name="Need of wet cleaning",
                                        help_text="Applies just for big/wet cleaning.")
    car_next_inspection_date = models.DateField(verbose_name="Next inspection date")
    car_next_inspection_km = models.DecimalField(decimal_places=0, max_digits=10, verbose_name="Next inspection KMs")
    car_next_oil_date = models.DateField(verbose_name="Next oil change date")
    car_next_oil_km = models.DecimalField(decimal_places=0, max_digits=10, verbose_name="Next oil change KMs")
    car_next_stk_date = models.DateField(blank=True, null=True, verbose_name="Next STK date")
    car_last_check = models.DateField(blank=True, null=True, verbose_name="Last check")
    car_actual_driven_kms = models.DecimalField(decimal_places=0, max_digits=10, verbose_name="Driven KMs")
    car_note = models.TextField(blank=True, max_length=1024, verbose_name="Notes")
    history = HistoricalRecords()

    def next_oil_or_inspection_date(self):
        return min(self.car_next_inspection_date, self.car_next_oil_date) if self.car_id else "0"

    next_oil_or_inspection_date.short_description = "Next 🔧 date"

    def next_oil_or_inspection_kms(self):
        return (int(min(self.car_next_oil_km, self.car_next_inspection_km)) - int(self.car_actual_driven_kms)) \
            if self.car_id else "0"

    next_oil_or_inspection_kms.short_description = "Next 🔧 kms"

    def get_absolute_url(self):
        return reverse("cars:car_detail", kwargs={'pk': self.pk, "city": self.car_city.pk})

    def __str__(self):
        return self.car_name

    def do_check(self):
        self.car_last_check = timezone.now()
        self.save()

    car_next_date = property(next_oil_or_inspection_date)
    car_next_km = property(next_oil_or_inspection_kms)
