# Generated by Django 3.0.4 on 2020-03-30 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0002_auto_20200330_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorized',
            name='last_edited',
        ),
    ]
