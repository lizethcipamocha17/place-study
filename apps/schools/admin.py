from django.contrib import admin

from .models import School, Content, Comment


# Register your models here.

class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'school_id']


#     ordering = ['-category_id']
#     search_fields = ['category_id__name_category']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text']


admin.site.register(School)
admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)
