from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, help_text="Short descriptive unique name for use in urls.")
    # editable=False
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
    product_likes = models.IntegerField(default=0, editable=False)
    liked_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    comments_text = models.TextField(verbose_name='Comment text')
    comments = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('Created', null=True, blank=True, auto_now_add=True)
