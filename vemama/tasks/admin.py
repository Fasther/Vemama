from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "car",
                    "user",
                    "due_date",
                    "is_completed",
    ]
    readonly_fields = ["created_date", "is_completed"]
    raw_id_fields = ["car"]


admin.site.register(Task, TaskAdmin)
