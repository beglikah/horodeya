from django.contrib import admin
from documents import models


# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'doc_name')
    fields = [
        'title',
        'slug',
        'document'
    ]
    search_fields = ['title', 'content']
    ordering = ['-pub_date']
    date_hierarchy = 'pub_date'


admin.site.register(models.Document, DocumentAdmin)
