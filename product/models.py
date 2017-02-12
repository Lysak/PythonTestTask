from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, help_text="Short descriptive unique name for use in urls.")  # editable=False
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, help_text="Short descriptive unique name for use in urls.")
    description = models.TextField(max_length=200, null=True, blank=True)
    price = models.DecimalField('Price $', max_digits=8, decimal_places=2)
    created_at = models.DateTimeField('Created')  # auto_now_add=True
    modified_at = models.DateTimeField('Modified', auto_now=True)

    def __str__(self):
        return self.name
