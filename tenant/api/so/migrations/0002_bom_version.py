# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('so', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bom',
            name='version',
            field=models.IntegerField(blank=True, db_column='veision', null=True, verbose_name='版本号'),
        ),
    ]
