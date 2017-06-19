# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0006_article_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='landing_article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wiki.Article'),
        ),
    ]