# Generated by Django 2.2.6 on 2020-01-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PipeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.TextField()),
                ('b', models.TextField()),
                ('c', models.TextField()),
                ('ts', models.TextField()),
                ('count', models.TextField()),
                ('weight', models.TextField()),
                ('ps', models.TextField()),
            ],
        ),
    ]