from django.contrib import admin
from .models import City, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ["car_name",
                    "car_id",
                    "car_city",
                    "car_last_check",
                    "car_next_date",
                    "car_next_km",
                    ]
    readonly_fields = ["car_next_date",
                       "car_next_km",
                       ]


admin.site.register(City)
admin.site.register(Car, CarAdmin)