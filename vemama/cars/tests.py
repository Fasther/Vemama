from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import resolve

from cars.models import *


class CityTests(TestCase):

    def setUp(self) -> None:
        super().__init__()
        self.test_user = get_user_model().objects.create(username="test_user")

    def test_city_create(self):
        city = City.objects.create(name="Brno")
        self.assertIsNotNone(city)
        self.assertAlmostEqual(1, len(City.objects.all()))

    def test_get_url(self):
        city = City.objects.create(name="Test City")
        url = city.get_absolute_url()
        # try to get object from url
        url_city = City.objects.get(pk=resolve(url).kwargs.get("city"))
        self.assertEqual(city, url_city)

    def test_city_in_cities_page(self):
        city = City.objects.create(name="Test City")
        cities_url = "/cars/"
        c = Client()
        c.force_login(self.test_user)
        response = c.get(cities_url)
        self.assertContains(response, city.name, status_code=200)
