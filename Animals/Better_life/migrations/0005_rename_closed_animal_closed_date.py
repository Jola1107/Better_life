# Generated by Django 3.2 on 2022-07-14 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Better_life', '0004_auto_20220714_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='closed',
            new_name='closed_date',
        ),
    ]
