from django.contrib import admin
from .models import City, Car


class CarAdmin(admin.ModelAdmin):
    list_display = ["car_name",
                    "car_id",
                    "car_city",
                    "car_actual_driven_kms",
                    "car_last_check",
                    "car_next_km",
                    "car_next_date",
                    ]
    list_editable = ["car_actual_driven_kms", ]
    readonly_fields = ["car_next_date",
                       "car_next_km",
                       ]
    list_filter = ["car_city"]
    search_fields = ["car_name"]


admin.site.register(City)
admin.site.register(Car, CarAdmin)
