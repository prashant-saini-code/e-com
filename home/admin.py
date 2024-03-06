from django.contrib import admin

from home.models import Category, Product, Tag

# Register your models here.
admin.site.register((Category, Tag, Product))
