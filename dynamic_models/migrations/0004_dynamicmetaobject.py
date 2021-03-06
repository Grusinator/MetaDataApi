# Generated by Django 2.1.15 on 2020-02-20 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0019_datafetch_data_provider'),
        ('mutant', '0001_initial'),
        ('dynamic_models', '0003_dummy'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicMetaObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_provider',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataproviders.DataProvider')),
                ('dynamic_model',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mutant.ModelDefinition')),
            ],
        ),
    ]
