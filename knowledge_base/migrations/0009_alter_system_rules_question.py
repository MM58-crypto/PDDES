# Generated by Django 4.1.5 on 2023-02-22 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0007_remove_question_question_num'),
        ('knowledge_base', '0008_system_rules_choice_system_rules_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_rules',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='ui.question'),
        ),
    ]
