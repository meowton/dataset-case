from django.contrib import admin

from DataMatcher.models import DataTable, FileUpload


# Register your models here.
class TableDetails(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "cpf")
    list_filter = (
        "user",
        "first_name",
        "last_name",
    )


admin.site.register(DataTable, TableDetails)
admin.site.register(FileUpload)
