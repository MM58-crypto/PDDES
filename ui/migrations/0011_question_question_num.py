# Generated by Django 4.1.5 on 2023-03-05 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0010_remove_question_question_num_question_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_num',
            field=models.IntegerField(null=True),
        ),
    ]
