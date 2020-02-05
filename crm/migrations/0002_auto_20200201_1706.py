# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-02-01 09:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户列表', 'verbose_name_plural': '客户列表'},
        ),
        migrations.AlterField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='班主任'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='class_list',
            field=models.ManyToManyField(blank=True, to='crm.ClassList', verbose_name='意向班级'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campuses', verbose_name='校区'),
        ),
    ]
