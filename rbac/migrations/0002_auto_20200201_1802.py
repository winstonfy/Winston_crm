# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-01 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=128, verbose_name='权限'),
        ),
    ]
