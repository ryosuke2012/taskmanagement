# Generated by Django 5.0.6 on 2024-06-02 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, verbose_name='ステータス')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=20, verbose_name='タスク名')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='作成日時')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='完了日時')),
                ('deleted_flg', models.BooleanField(default=False, verbose_name='削除フラグ')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.status', verbose_name='ステータス')),
            ],
        ),
    ]
