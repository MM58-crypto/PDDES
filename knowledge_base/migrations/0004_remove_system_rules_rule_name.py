# Generated by Django 4.1.5 on 2023-02-11 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_base', '0003_remove_system_rules_symptom_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system_rules',
            name='rule_name',
        ),
    ]