from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "car",
                    "user",
                    "city",
                    "due_date",
                    "completed",
                    "completed_date",
    ]
    readonly_fields = ["created_date", "completed", "is_past_due",]
    raw_id_fields = ["car", ]
    list_filter = ["city", "completed", "user"]


admin.site.register(Task, TaskAdmin)
