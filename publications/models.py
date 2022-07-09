from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Publication(models.Model):
