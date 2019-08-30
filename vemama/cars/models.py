from django.db import models
from django.urls import reverse
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cars:car_list", kwargs={'city': self.pk})

    class Meta:
        verbose_name_plural = "Cities"


class Car(models.Model):
    car_name = models.CharField(max_length=200, unique=True)
    car_id = models.DecimalField(unique=True, decimal_places=0, max_digits=5)
    car_city = models.ForeignKey(City, related_name="cars", on_delete=models.CASCADE, verbose_name="City")
    car_next_inspection_date = models.DateField()
    car_next_inspection_km = models.DecimalField(decimal_places=0, max_digits=10)
    car_next_oil_date = models.DateField()
    car_next_oil_km = models.DecimalField(decimal_places=0, max_digits=10)
    car_last_check = models.DateField()
    car_actual_driven_kms = models.DecimalField(decimal_places=0, max_digits=10)
    car_note = models.TextField(blank=True, max_length=1024)

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
