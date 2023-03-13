# Generated by Django 4.1.5 on 2023-01-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_base', '0002_alter_disorder_diagnosis_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system_rules',
            name='symptom',
        ),
        migrations.AddField(
            model_name='disorder_diagnosis',
            name='symptoms',
            field=models.ManyToManyField(to='knowledge_base.psych_d_symptoms'),
        ),
        migrations.AlterField(
            model_name='disorder_diagnosis',
            name='disorder_name',
            field=models.CharField(max_length=255),
        ),
    ]