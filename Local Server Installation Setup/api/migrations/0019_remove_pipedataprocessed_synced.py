# Generated by Django 3.1 on 2020-09-05 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200619_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipedataprocessed',
            name='synced',
        ),
    ]
