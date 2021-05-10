from django.contrib import admin

from .models import School, Category, Content


# Register your models here.
class ContentAdmin(admin.ModelAdmin):
    list_display = ('name_content', 'description', 'image',)
    list_filter = ('category_id__name_category')
    ordering = ('-category_id')
    search_fields = ('category_id__name_category')


admin.site.register(School)
admin.site.register(Category)
admin.site.register(Content)
