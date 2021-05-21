from django.contrib import admin
from .models import User, Location


# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'email', 'school', 'location']
#     list_filter = ['location__name_department', 'school__name_school']
#     ordering = ['-school', '-location']
#     search_fields = ['location__name_location', 'school__name_school']
#     list_per_page = 10


admin.site.register(Location)
admin.site.register(User)
