# Generated by Django 4.1.5 on 2023-02-23 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0008_question_question_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='id',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_num',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
