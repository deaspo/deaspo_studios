# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-10 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deaspo', '0026_auto_20170110_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productweborder',
            name='posted_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='usernext',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
