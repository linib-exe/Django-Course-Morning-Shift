# Generated by Django 4.2.11 on 2024-03-17 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_alter_todo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='user',
        ),
    ]