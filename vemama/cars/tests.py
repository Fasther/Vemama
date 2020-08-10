from django.test import TestCase

from cars.models import *


class CityTests(TestCase):
    def test_city_create(self):
        city = City.objects.create(name="Brno")
        self.assertIsNotNone(city)
        self.assertAlmostEqual(1, len(City.objects.all()))
