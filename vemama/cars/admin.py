from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import City, Car


class CarAdmin(SimpleHistoryAdmin):
    list_display = ["car_name",
                    "car_id",
                    "car_city",
                    "car_actual_driven_kms",
                    "car_last_check",
                    "car_next_km",
                    "car_next_date",
                    ]
    list_editable = ["car_actual_driven_kms", ]
    history_list_display = ["car_actual_driven_kms", ]
    readonly_fields = ["car_next_date",
                       "car_next_km",
                       ]
    list_filter = ["car_city"]
    search_fields = ["car_name"]

    @staticmethod
    def changed_fields(obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

admin.site.register(City)
admin.site.register(Car, CarAdmin)
