from django.contrib import admin

from .models import School, Content


# Register your models here.

# class ContentAdmin(admin.ModelAdmin):
#     list_display = ['name_content', 'description', 'image']
#     ordering = ['-category_id']
#     search_fields = ['category_id__name_category']


admin.site.register(School)
admin.site.register(Content)
