# Generated by Django 4.1.5 on 2023-02-12 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_alter_questions_question_text_delete_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ui.question')),
            ],
        ),
    ]
