# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-06 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_auto_20170205_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='expire_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Válido até'),
        ),
    ]
