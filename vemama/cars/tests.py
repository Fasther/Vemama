from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import resolve

from cars.models import *


class CityTests(TestCase):

    def setUp(self) -> None:
        super().__init__()
        self.test_user = get_user_model().objects.create(username="test_user")

    def test_city_create(self):
        city = City.objects.create(name="Brno", )
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

    def test_city_intervals(self):
        city = City.objects.create(name="Brno", )
        city.car_routine_check_interval = 30
        city.car_task_due_days = 8
        city.save()
        # test if data is same
        city = City.objects.get(name="Brno")
        self.assertEqual(city.car_routine_check_interval, 30)
        self.assertEqual(city.car_task_due_days, 8)


class CarTests(TestCase):
    # TODO implement all tests
    def setUp(self) -> None:
        super().__init__()
        self.test_user = get_user_model().objects.create(username="test_user")
        # TODO create test city
        # TODO create test car

    def test_needs_attention(self):
        pass

    def test_car_needs_check(self):
        pass

    def test_car_str(self):
        pass

    def test_do_check(self):
        pass

    def test_needs_check(self):
        pass

    def test_needs_cleaning(self):
        pass

    def test_needs_service(self):
        pass

    def test_needs_stk(self):
        pass

    def test_needs_tyres_switch(self):
        pass
