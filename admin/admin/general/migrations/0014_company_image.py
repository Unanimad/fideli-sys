# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 22:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0013_auto_20170210_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
