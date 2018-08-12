# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-01 23:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0025_auto_20180701_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corpus',
            name='id',
        ),
        migrations.AddField(
            model_name='corpus',
            name='simplemetadata_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='metadata.SimpleMetadata'),
            preserve_default=False,
        ),
    ]
