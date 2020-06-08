from datetime import timedelta

from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils import timezone
from cars.managers import ActiveCarManager
from simple_history.models import HistoricalRecords
from django.conf import settings


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cars:car_list", kwargs={'city': self.pk})

    class Meta:
        verbose_name_plural = "Cities"


class Car(models.Model):
    # Car tyres definition
    TYRE_ALL_YEAR = 1
    TYRE_SUMMER = 2
    TYRE_WINTER = 3
    CAR_TYRES = (
        (1, "All year"),
        (2, "Summer"),
        (3, "Winter")
    )

    # Dirtiness definition

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
    car_next_date = models.DateField(blank=True, null=True, verbose_name="Next 🔧 date")
    car_next_km = models.DecimalField(blank=True, null=True, decimal_places=0, max_digits=10,
                                      verbose_name="Next 🔧 kms")
    car_note = models.TextField(blank=True, max_length=1024, verbose_name="Notes",
                                help_text="This is just for internal notes and tips.\n If you want to report some"
                                          " damage or problem, please inform responsible person.")
    history = HistoricalRecords()

    objects = Manager()
    active = ActiveCarManager()

    def _next_oil_or_inspection_date(self):
        return min(self.car_next_inspection_date, self.car_next_oil_date) if self.car_id else timezone.now()

    def _next_oil_or_inspection_kms(self):
        return (int(min(self.car_next_oil_km, self.car_next_inspection_km)) - int(self.car_actual_driven_kms)) \
            if self.car_id else "0"

    def get_absolute_url(self):
        return reverse("cars:car_detail", kwargs={'pk': self.pk, "city": self.car_city.pk})

    def __str__(self):
        return f"{self.car_name} ({self.car_city})"

    def do_check(self):
        self.car_last_check = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.car_next_date = self._next_oil_or_inspection_date()
        self.car_next_km = self._next_oil_or_inspection_kms()
        super().save(*args, **kwargs)

    @property
    def needs_check(self):
        time_from_last_check = timezone.now().date() - self.car_last_check
        if time_from_last_check > timedelta(days=settings.ROUTINE_CHECK_INTERVAL):
            return True
        else:
            return False
        pass

    @property
    def needs_cleaning(self):
        if self.car_dirtiness == 3:
            return True
        else:
            return False

    @property
    def needs_service(self):
        needs_service = False
        # check date:
        next_date = self._next_oil_or_inspection_date()
        days_till_service = next_date - timezone.now().date()
        if days_till_service < timedelta(days=settings.CAR_SERVICE_DAYS_THRESHOLD):
            needs_service = True
        # check kms
        if settings.CAR_SERVICE_KM_THRESHOLD > self._next_oil_or_inspection_kms():
            needs_service = True
        return needs_service

    @property
    def needs_stk(self):
        next_date = self.car_next_stk_date
        if not next_date:
            return False
        days_till_stk = next_date - timezone.now().date()
        if days_till_stk < timedelta(days=settings.CAR_SERVICE_DAYS_THRESHOLD):
            return True
        else:
            return False

    @property
    def needs_tyres_switch(self):
        if self.car_tyres == Car.TYRE_ALL_YEAR:
            return False

        winter_tyre_months = ("11", "12", "01", "02", "03")
        # we want to generate notification one month before.
        current_month = (timezone.now() + timedelta(weeks=4)).strftime("%m")
        if current_month in winter_tyre_months:  # it is winter time! ❄
            if self.car_tyres in (Car.TYRE_SUMMER, Car.TYRE_ALL_YEAR):
                return True
            else:
                return False
        else:
            if self.car_tyres == Car.TYRE_WINTER:
                return True
            else:
                return False

    @property
    def needs_attention(self):
        return any((self.needs_service, self.needs_check, self.needs_tyres_switch,
                    self.needs_cleaning, self.needs_stk))
