# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 16:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deaspo', '0005_emailplan_productweborder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='pn_monthly',
            new_name='pn_yearly',
        ),
        migrations.AlterField(
            model_name='productweborder',
            name='posted_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 23, 19, 58, 22, 340000), editable=False),
        ),
    ]
