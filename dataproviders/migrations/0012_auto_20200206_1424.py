# Generated by Django 2.1.15 on 2020-02-06 13:24

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0011_auto_20200206_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='label_info',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafileupload',
            name='data_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datafileupload',
                                    to='dataproviders.DataProvider'),
        ),
    ]
