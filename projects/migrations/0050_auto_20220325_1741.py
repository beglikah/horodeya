# Generated by Django 3.1.1 on 2022-03-25 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0049_auto_20220312_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='community',
        ),
        migrations.RemoveField(
            model_name='user',
            name='communities',
        ),
        migrations.DeleteModel(
            name='Community',
        ),
    ]
