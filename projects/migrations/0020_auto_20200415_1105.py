# Generated by Django 2.2.8 on 2020-04-15 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20200413_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneysupport',
            name='supportType',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='thingsupport',
            name='supportType',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='timesupport',
            name='supportType',
            field=models.CharField(max_length=30, null=True),
        ),
    ]