# Generated by Django 2.2.8 on 2020-04-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20200423_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='revolut_phone',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True),
        ),
    ]