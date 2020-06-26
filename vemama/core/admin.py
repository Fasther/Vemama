from django.contrib import admin

from core.models import Profile, Person


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user",)
    search_fields = ("user",)
    list_display = ("user", "cities_list", "active_tasks")

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(user__is_active=True)

    def cities_list(self, obj):
        return ", ".join(str(city) for city in obj.cities.all())

    cities_list.short_description = "Cities"

    @staticmethod
    def active_tasks(obj):
        return len(obj.user.tasks.filter(completed=False))


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name", "last_name")
    list_display = ("__str__", "email", "is_active", "is_staff")
    list_filter = ("is_active",)
    readonly_fields = ("last_login", "date_joined", "password",)
    fields = ("username", "is_active", "email", "first_name", "last_name", "groups", "user_permissions",
              "is_superuser", "date_joined", "last_login", "password",)


# admin.site.unregister(User)
# admin.site.unregister(Group)

admin.site.site_header = "Vemama, takes care"
admin.site.site_title = "Vemama Admin"
admin.site.index_title = "Main Crossroad"
