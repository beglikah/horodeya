# Generated by Django 2.2.6 on 2019-10-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='type',
            field=models.CharField(choices=[('b', 'business'), ('c', 'cause')], default='c', max_length=1),
            preserve_default=False,
        ),
    ]
