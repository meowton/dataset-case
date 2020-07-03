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
