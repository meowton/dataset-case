from django.contrib import admin

from DataMatcher.models import DataTable, FileUpload


# Register your models here.
class TableDetails(admin.ModelAdmin):
    list_display = ("id",
                    "user",
                    "cpf",
                    "first_name",
                    "last_name")
    list_filter = (
        "date_registered",
        "is_active",
        "country",
    )


class FileDetails(admin.ModelAdmin):
    list_display = ('id',
                    'file',
                    'description',
                    'uploaded_at')
    list_filter = ['uploaded_at']


admin.site.register(DataTable, TableDetails)
admin.site.register(FileUpload, FileDetails)
