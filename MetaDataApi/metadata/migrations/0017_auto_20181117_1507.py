# Generated by Django 2.1.3 on 2018-11-17 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0016_auto_20181117_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attribute',
            old_name='datatype',
            new_name='data_type',
        ),
        migrations.RenameField(
            model_name='attribute',
            old_name='dataunit',
            new_name='data_unit',
        ),
    ]
