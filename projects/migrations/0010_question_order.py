# Generated by Django 2.2.8 on 2020-02-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20200208_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]