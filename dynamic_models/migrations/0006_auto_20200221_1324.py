# Generated by Django 2.1.15 on 2020-02-21 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_models', '0005_auto_20200220_1855'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dummy',
        ),
        migrations.AlterField(
            model_name='dynamicmetaobject',
            name='dynamic_model',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meta_object',
                                       to='mutant.ModelDefinition'),
        ),
    ]
