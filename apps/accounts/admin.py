from django.contrib import admin
from .models import User, Location,Log


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

    #     list_filter = ['location__name_department', 'school__name_school']
    #     ordering = ['-school', '-location']
    #     search_fields = ['location__name_location', 'school__name_school']
    #     list_per_page = 10
    def save_model(self, request, obj, form, change):
        if obj.password.startswith('pbkdf2'):
            obj.password = obj.password
        else:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(Location)
admin.site.register(User, UserAdmin)
admin.site.register(Log)
