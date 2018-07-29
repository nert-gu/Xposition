# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-24 21:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wiki.plugins.metadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0016_auto_20180724_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('simplemetadata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='metadata.SimpleMetadata')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Corpus Name')),
                ('version', models.CharField(max_length=200, null=True, validators=[wiki.plugins.metadata.models.version_validator], verbose_name='Version')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('genre', models.CharField(blank=True, max_length=200, verbose_name='Corpus Genre')),
                ('description', models.CharField(blank=True, help_text='Include number of tokens and basic statistics', max_length=300, verbose_name='Description')),
                ('languages', models.CharField(max_length=200, null=True, verbose_name='Language(s)')),
            ],
            options={
                'verbose_name': 'corpus',
                'verbose_name_plural': 'corpora',
                'ordering': ['name', 'version'],
            },
            bases=('metadata.simplemetadata',),
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
                ('tokens', wiki.plugins.metadata.models.StringListField(max_length=1000, null=True, verbose_name='Tokens')),
                ('word_gloss', wiki.plugins.metadata.models.StringListField(blank=True, max_length=200, verbose_name='Word Gloss')),
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
                ('token_indices', wiki.plugins.metadata.models.IntListField(blank=True, max_length=200, verbose_name='Token Indices')),
                ('obj_case', models.PositiveIntegerField(blank=True, choices=[(1, 'Unknown'), (2, 'Nominative'), (4, 'Accusative'), (8, 'Ergative'), (16, 'Absolutive'), (32, 'NominativeSOnly'), (64, 'Dative'), (128, 'Benefactive'), (256, 'Purposive'), (512, 'Genitive'), (1024, 'Relative'), (2048, 'Partitive'), (4096, 'Instrumental'), (8192, 'Comitative'), (16384, 'Vocative'), (32768, 'Comparative'), (65536, 'Equative'), (131072, 'Privative'), (262144, 'Proprietive'), (524288, 'Aversive'), (1048576, 'Formal'), (2097152, 'Translative'), (4194304, 'EssiveModal'), (8388608, 'Distal'), (16777216, 'Proximate'), (33554432, 'Essive'), (67108864, 'Allative'), (134217728, 'Ablative'), (268435456, 'Approximative'), (536870912, 'Terminative')])),
                ('obj_head', models.CharField(max_length=200, null=True, verbose_name='Object Head')),
                ('gov_head', models.CharField(max_length=200, null=True, verbose_name='Governor Head')),
                ('gov_obj_syntax', models.CharField(max_length=200, null=True, verbose_name='Governor-Object Syntax')),
                ('gov_head_index', models.PositiveIntegerField(null=True, verbose_name='Governor Index')),
                ('obj_head_index', models.PositiveIntegerField(null=True, verbose_name='Object Index')),
                ('adp_pos', models.CharField(blank=True, max_length=200, verbose_name='Adposition Part of Speech')),
                ('gov_pos', models.CharField(blank=True, max_length=200, verbose_name='Governor Part of Speech')),
                ('obj_pos', models.CharField(blank=True, max_length=200, verbose_name='Object Part of Speech')),
                ('gov_supersense', models.CharField(blank=True, max_length=200, verbose_name='Governor Supersense')),
                ('obj_supersense', models.CharField(blank=True, max_length=200, verbose_name='Object Supersense')),
                ('is_gold', models.BooleanField(default=False, verbose_name='Gold Annotation?')),
                ('annotator_cluster', models.CharField(blank=True, help_text='Informal Label for Grouping Similar Tokens', max_length=200, verbose_name='Annotator Cluster')),
                ('is_transitive', models.BooleanField(default=True, help_text='Does the adposition take an object?', verbose_name='Transitive?')),
                ('is_typo', models.BooleanField(default=False, verbose_name='Typo?')),
                ('is_abbr', models.BooleanField(default=False, verbose_name='Abbreviation?')),
                ('mwe_subtokens', wiki.plugins.metadata.models.StringListField(blank=True, max_length=200, verbose_name='MWE Subtokens')),
                ('main_subtoken_indices', wiki.plugins.metadata.models.IntListField(blank=True, max_length=200, null=True, verbose_name='Main Subtoken Indices')),
                ('main_subtoken_string', wiki.plugins.metadata.models.StringListField(blank=True, max_length=200, null=True, verbose_name='Main Subtoken String')),
                ('adposition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Adposition')),
            ],
            options={
                'verbose_name': 'adposition token annotation',
                'ordering': ['sentence', 'token_indices'],
            },
        ),
        migrations.AlterModelOptions(
            name='construal',
            options={'ordering': ['role', 'function', 'special'], 'verbose_name': 'construal'},
        ),
        migrations.AddField(
            model_name='adpositionrevision',
            name='is_pp_idiom',
            field=models.BooleanField(default=False, verbose_name='Is PP Idiom?'),
        ),
        migrations.AddField(
            model_name='construal',
            name='special',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='adpositionrevision',
            name='other_forms',
            field=wiki.plugins.metadata.models.StringListField(blank=True, help_text='Exclude typos, Separate by spaces', max_length=200, null=True, verbose_name='Other spellings or inflections'),
        ),
        migrations.AlterField(
            model_name='construal',
            name='function',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rfs_with_function', to='metadata.Supersense'),
        ),
        migrations.AlterField(
            model_name='construal',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rfs_with_role', to='metadata.Supersense'),
        ),
        migrations.AlterField(
            model_name='metadatarevision',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='construal',
            unique_together=set([('role', 'function', 'special')]),
        ),
        #migrations.AlterUniqueTogether(
        #    name='usagerevision',
        #    unique_together=set([]),
        #),
        migrations.AddField(
            model_name='ptokenannotation',
            name='construal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ptoken_with_construal', to='metadata.Construal'),
        ),
        migrations.AddField(
            model_name='ptokenannotation',
            name='sentence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.CorpusSentence'),
        ),
        migrations.AddField(
            model_name='ptokenannotation',
            name='usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Usage'),
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