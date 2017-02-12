from django.contrib import admin

from .models import Category
from .models import Product


class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryProductAdmin)
admin.site.register(Product, CategoryProductAdmin)
