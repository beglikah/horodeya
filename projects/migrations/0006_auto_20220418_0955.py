# Generated by Django 3.1.1 on 2022-04-18 06:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_auto_20220409_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='administrators',
            field=models.ManyToManyField(blank=True, related_name='administrator_of_project', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_of_project', to=settings.AUTH_USER_MODEL),
        ),
    ]