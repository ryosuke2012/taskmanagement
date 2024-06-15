# Generated by Django 5.0.6 on 2024-06-15 03:45

import django.db.models.deletion
import todo.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.status', validators=[todo.models.validate_status_id], verbose_name='ステータス'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=20, validators=[todo.models.validate_task_name], verbose_name='タスク名'),
        ),
    ]