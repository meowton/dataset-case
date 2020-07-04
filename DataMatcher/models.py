from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class DataTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    account_number = models.IntegerField()
    digit = models.IntegerField()
    cpf = models.CharField(max_length=12)
    address = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    credit_card = models.CharField(max_length=14, blank=True, null=True)
    is_active = models.BooleanField()
    date_registered = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Tables"

    def __str__(self):
        return self.first_name


class FileUpload(models.Model):
    dir_to_upload = 'tables/'
    description = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to=dir_to_upload)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return self.file.name.replace(self.dir_to_upload, '')

    def get_file_date(self):
        return self.uploaded_at.strftime("%d/%m/%Y, %H:%M")

    def get_file_date_str(self):
        return self.uploaded_at.strftime("%Y-%m-%dT%H:%M")

    def get_file_url(self):
        return self.file.url

    def __str__(self):
        return f'{self.get_file_name()} - {self.get_file_date()}'
