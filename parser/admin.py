from django.contrib import admin

from parser.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploadedFile', 'dateTimeOfUpload')