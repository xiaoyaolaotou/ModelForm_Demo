from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.Book)
admin.site.register(models.Publish)
admin.site.register(models.Author)