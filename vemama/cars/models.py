from django.db import models


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_name = models.CharField(max_length=200, unique=True)
    car_id = models.DecimalField(unique=True, decimal_places=0, max_digits=5)
    car_city = models.ForeignKey(City, related_name="city", on_delete=models.CASCADE)
    car_next_inspection_date = models.DateField()
    car_next_inspection_km = models.DecimalField(decimal_places=0, max_digits=10)
    car_next_oil_date = models.DateField()
    car_next_oil_km = models.DecimalField(decimal_places=0, max_digits=10)
    car_last_check = models.DateTimeField()
    car_note = models.CharField(blank=True, max_length=1024)

    def next_oil_or_inspection_date(self):
        return min(self.car_next_inspection_date, self.car_next_oil_date) if self.car_id else "0"

    # def next_oil_or_inspection_km(self):
    #     return min(self.car_next_inspection_km, self.car_next_oil_km)

    def __str__(self):
        return self.car_name

    car_next_date = property(next_oil_or_inspection_date)