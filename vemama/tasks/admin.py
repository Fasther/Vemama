from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Task


class TaskAdmin(SimpleHistoryAdmin):
    list_display = ["__str__",
                    "car",
                    "user",
                    "city",
                    "due_date",
                    "completed",
                    "completed_date",
                    ]
    readonly_fields = ["created_date", "completed", "is_past_due", "city", ]
    autocomplete_fields = ["car", "user"]
    search_fields = ["name", "car__car_name"]
    history_list_display = ["completed", "changed_fields"]
    raw_id_fields = ["car", ]
    list_filter = ["city", "completed", "task_type", "user", "car__car_name"]

    @staticmethod
    def changed_fields(obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None


admin.site.register(Task, TaskAdmin)
