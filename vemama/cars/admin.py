from django.contrib import admin
from .models import City, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ["car_name",
                    "car_id",
                    "car_city",
                    "car_next_inspection_date",
                    "car_next_inspection_km",
                    "car_next_oil_date",
                    "car_next_oil_km",
                    "car_last_check",
                    "car_note",
                    "car_next_date"
                    ]
    readonly_fields = ["car_next_date"]


admin.site.register(City)
admin.site.register(Car, CarAdmin)