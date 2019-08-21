from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "car",
                    "user",
                    "due_date",
                    "completed_date",

    ]
    readonly_fields = ["created_date"]
    raw_id_fields = ["car"]


admin.site.register(Task, TaskAdmin)
