# Generated by Django 2.2.2 on 2019-06-10 06:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0003_auto_20190610_0849'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataproviderprofile',
            old_name='provider',
            new_name='data_provider',
        ),
        migrations.AlterUniqueTogether(
            name='dataproviderprofile',
            unique_together={('data_provider', 'profile')},
        ),
        migrations.RemoveField(
            model_name='dataproviderprofile',
            name='profile_json_field',
        ),
    ]
