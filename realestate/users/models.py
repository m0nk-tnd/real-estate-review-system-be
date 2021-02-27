from django.db import models
from django.contrib.auth.models import User


class BaseUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    birth_date = models.DateField(verbose_name='Date of birth')

    class Meta:
        abstract = True
