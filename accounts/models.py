from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    phone = models.DecimalField(
        max_digits=15, decimal_places=0,
        null=False, blank=False, verbose_name='Телефон',
        default='87777777777'
    )
