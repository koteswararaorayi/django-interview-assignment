from django.db import models

class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    email = models.EmailField(unique=True, max_length=32)
    phone_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=16)
    address = models.TextField()

    class Meta:
        db_table = "employee"

    def __str__(self):
        return str(id)
