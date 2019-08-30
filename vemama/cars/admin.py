from django.contrib import admin
from .models import City, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ["car_name",
                    "car_city",
                    "car_last_check",
                    "car_actual_driven_kms",
                    "car_next_km",
                    "car_next_date",
                    ]
    list_editable = ["car_actual_driven_kms", ]
    readonly_fields = ["car_next_date",
                       "car_next_km",
                       "next_oil_or_inspection_date",
                       ]
    list_filter = ["car_city"]


admin.site.register(City)
admin.site.register(Car, CarAdmin)
