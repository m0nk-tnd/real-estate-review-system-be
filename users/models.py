import uuid as uuid
from django.db import models
from django.contrib.auth.models import User


class BaseUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(verbose_name='Date of birth')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TenantProfile(BaseUserProfile):
    pass

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class LandlordProfile(BaseUserProfile):
    pass

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
