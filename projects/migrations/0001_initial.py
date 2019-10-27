# Generated by Django 2.2.6 on 2019-10-20 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('edited_at', models.DateTimeField(editable=False)),
                ('type', models.CharField(choices=[('b', 'business'), ('c', 'cause')], max_length=1)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('published', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('edited_at', models.DateTimeField(editable=False)),
                ('text', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
