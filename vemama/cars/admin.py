from django.contrib import admin
from .models import City, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ["car_name",
                    "car_city",
                    "car_last_check",
                    "car_actual_driven_kms",
                    "next_oil_or_inspection_date",
                    "next_oil_or_inspection_kms",
                    ]
    list_editable = ["car_actual_driven_kms", ]
    readonly_fields = ["car_next_date",
                       "car_next_km",
                       ]


admin.site.register(City)
admin.site.register(Car, CarAdmin)