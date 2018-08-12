# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-02 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0029_auto_20180701_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptokenannotation',
            name='adposition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Adposition'),
        ),
        migrations.AlterField(
            model_name='ptokenannotation',
            name='construal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ptoken_with_construal', to='metadata.Construal'),
        ),
        migrations.AlterField(
            model_name='ptokenannotation',
            name='usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Usage'),
        ),
    ]
