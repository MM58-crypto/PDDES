# Generated by Django 4.1.5 on 2023-04-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_base', '0008_disorder_diagnosis_recommendation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disorder_diagnosis',
            name='disorder_name',
            field=models.CharField(choices=[('social_anxiety', 'Social anxiety'), ('bipolar disorder', 'bipolar disorder'), ('ptsd', 'PTSD'), ('depression', 'Depression'), ('obsessive_compulsive', 'Obsessive Compulsive'), ('anti_social', 'Anti-Social personality disorder'), ('anxiety', 'Anxiety'), ('schizophrenia', 'Schizophrenia')], default='social_anxiety', max_length=255),
        ),
    ]