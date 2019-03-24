# Generated by Django 2.1.7 on 2019-03-24 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20190324_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foaf_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='profile', to='metadata.ObjectInstance'),
        ),
    ]
