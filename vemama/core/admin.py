from django.contrib import admin
from django.contrib.auth.models import User, Group

from core.models import Profile, Person


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user",)
    search_fields = ("user",)


@admin.register(Person)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name", "last_name")


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Vemama, takes care"
admin.site.site_title = "Vemama Admin"
admin.site.index_title = "Main Crossroad"
