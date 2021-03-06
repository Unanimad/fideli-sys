# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-04 15:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cartão',
                'verbose_name_plural': 'Cartões',
            },
        ),
        migrations.CreateModel(
            name='CardConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire', models.IntegerField()),
                ('limit', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Configuração do cartão',
                'verbose_name_plural': 'Configurações dos cartões',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('playStore', models.URLField()),
                ('appStore', models.URLField()),
                ('status', models.BooleanField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Company')),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Company'),
        ),
        migrations.AddField(
            model_name='cardconfiguration',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Company'),
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Client'),
        ),
        migrations.AddField(
            model_name='card',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Company'),
        ),
        migrations.AddField(
            model_name='card',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.CardConfiguration'),
        ),
        migrations.AddField(
            model_name='card',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Service'),
        ),
    ]
