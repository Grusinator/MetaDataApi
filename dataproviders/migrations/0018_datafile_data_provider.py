# Generated by Django 2.1.15 on 2020-02-20 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0017_auto_20200220_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='data_provider',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to='dataproviders.DataProvider'),
            preserve_default=False,
        ),
    ]
