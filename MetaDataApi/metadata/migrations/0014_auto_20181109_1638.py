# Generated by Django 2.1.2 on 2018-11-09 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0013_auto_20181029_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schema',
            name='label',
            field=models.TextField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='schema',
            unique_together=set(),
        ),
    ]
