from django.contrib import admin

from .models import Category
from .models import Product
from .models import Comment


class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductInline(admin.StackedInline):
    model = Comment
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_filter = ('created_at',)

admin.site.register(Category, CategoryProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.site_url = '/products'
