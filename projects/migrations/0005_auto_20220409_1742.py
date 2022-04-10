# Generated by Django 3.1.1 on 2022-04-09 14:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_auto_20220331_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='administrators',
            field=models.ManyToManyField(related_name='administrator_of_project', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='member_of_project', to=settings.AUTH_USER_MODEL),
        ),
    ]
