# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-05 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_company_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=16, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='company',
            name='appStore',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='company',
            name='playStore',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
    ]
