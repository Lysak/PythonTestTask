# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20170508_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created'),
        ),
    ]
