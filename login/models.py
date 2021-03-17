from django.db import models


# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField(primary_key=True)
    company = models.CharField(max_length=255)
    password = models.TextField()
    is_active = models.BooleanField(default=False)