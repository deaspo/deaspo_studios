# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-28 12:14
from __future__ import unicode_literals

import datetime
import deaspo.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deaspo', '0017_auto_20161227_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, max_length=3000)),
                ('picture', models.ImageField(default='profile.png', upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='ppics',
            field=models.ImageField(default='products/default.jpg', upload_to=deaspo.models.path_file_name),
        ),
        migrations.AlterField(
            model_name='productweborder',
            name='posted_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 28, 15, 14, 56, 46000), editable=False),
        ),
        migrations.AlterField(
            model_name='usernext',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 28, 15, 14, 56, 46000)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='profile.png', upload_to=deaspo.models.path_profile_image),
        ),
    ]