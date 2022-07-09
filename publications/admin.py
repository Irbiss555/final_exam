from django.contrib import admin

# Register your models here.
from publications.models import Publication, Category

admin.site.register(Publication)
admin.site.register(Category)
