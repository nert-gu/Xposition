# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-19 23:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0016_auto_20180619_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Corpus Name')),
                ('version', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Version')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('genre', models.CharField(blank=True, max_length=200, verbose_name='Corpus Genre')),
                ('description', models.CharField(blank=True, help_text='Include number of tokens and basic statistics', max_length=200, verbose_name='Description')),
                ('languages', models.CharField(max_length=200, null=True, verbose_name='Language(s)')),
            ],
            options={
                'verbose_name': 'corpus',
                'verbose_name_plural': 'corpora',
                'ordering': ['name', 'version'],
            },
        ),
        migrations.CreateModel(
            name='CorpusSentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_id', models.CharField(max_length=200, null=True, verbose_name='Sentence ID')),
                ('orthography', models.CharField(blank=True, help_text='language-specific details such as style of transliteration', max_length=200, verbose_name='Orthography')),
                ('is_parallel', models.BooleanField(default=False)),
                ('doc_id', models.CharField(max_length=200, null=True, verbose_name='Document ID')),
                ('text', models.CharField(max_length=1000, null=True, verbose_name='Text')),
                ('tokens', models.CharField(max_length=1000, null=True, verbose_name='Text')),
                ('word_gloss', models.CharField(blank=True, max_length=200, verbose_name='Word Gloss')),
                ('sent_gloss', models.CharField(blank=True, max_length=200, verbose_name='Sentence Gloss')),
                ('note', models.CharField(blank=True, max_length=200, verbose_name='Annotator Note')),
                ('mwe_markup', models.CharField(blank=True, max_length=200, verbose_name='MWE Markup')),
                ('corpus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corpus_sentences', to='metadata.Corpus')),
                ('language', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='corpus_sentences', to='metadata.Language')),
            ],
            options={
                'verbose_name': 'corpus sentence',
                'ordering': ['corpus', 'sent_id'],
            },
        ),
        migrations.CreateModel(
            name='PTokenAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_indices', models.CharField(blank=True, max_length=200, verbose_name='Token Indices')),
                ('obj_case', models.PositiveIntegerField(blank=True, choices=[(1, 'Unknown'), (2, 'Nominative'), (4, 'Accusative'), (8, 'Ergative'), (16, 'Absolutive'), (32, 'NominativeSOnly'), (64, 'Dative'), (128, 'Benefactive'), (256, 'Purposive'), (512, 'Genitive'), (1024, 'Relative'), (2048, 'Partitive'), (4096, 'Instrumental'), (8192, 'Comitative'), (16384, 'Vocative'), (32768, 'Comparative'), (65536, 'Equative'), (131072, 'Privative'), (262144, 'Proprietive'), (524288, 'Aversive'), (1048576, 'Formal'), (2097152, 'Translative'), (4194304, 'EssiveModal'), (8388608, 'Distal'), (16777216, 'Proximate'), (33554432, 'Essive'), (67108864, 'Allative'), (134217728, 'Ablative'), (268435456, 'Approximative'), (536870912, 'Terminative')])),
                ('obj_head', models.CharField(blank=True, max_length=200, verbose_name='Object Head')),
                ('gov_head', models.CharField(blank=True, max_length=200, verbose_name='Governor Head')),
                ('gov_obj_syntax', models.CharField(blank=True, max_length=200, verbose_name='Governor-Object Syntax')),
                ('adp_pos', models.CharField(blank=True, max_length=200, verbose_name='Adposition Part of Speech')),
                ('gov_pos', models.CharField(blank=True, max_length=200, verbose_name='Governor Part of Speech')),
                ('obj_pos', models.CharField(blank=True, max_length=200, verbose_name='Object Part of Speech')),
                ('gov_supersense', models.CharField(blank=True, max_length=200, verbose_name='Governor Supersense')),
                ('obj_supersense', models.CharField(blank=True, max_length=200, verbose_name='Object Supersense')),
                ('is_gold', models.BooleanField(default=False)),
                ('annotator_cluster', models.CharField(blank=True, help_text='Informal Label for Grouping Similar Tokens', max_length=200, verbose_name='Annotator Cluster')),
                ('adposition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adposition', to='metadata.Adposition')),
                ('construal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='construal', to='metadata.Construal')),
                ('sentence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sentence', to='metadata.CorpusSentence')),
                ('usage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usage', to='metadata.Usage')),
            ],
            options={
                'verbose_name': 'adposition token annotation',
                'ordering': ['sentence', 'token_indices'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='corpus',
            unique_together=set([('name', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='ptokenannotation',
            unique_together=set([('sentence', 'token_indices')]),
        ),
        migrations.AlterUniqueTogether(
            name='corpussentence',
            unique_together=set([('corpus', 'sent_id')]),
        ),
    ]
