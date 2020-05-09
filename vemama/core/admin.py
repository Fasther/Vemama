from django.contrib import admin
from django.contrib.auth.models import User

from core.models import Profile, Person


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("user",)


@admin.register(Person)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name", "last_name")


admin.site.unregister(User)
