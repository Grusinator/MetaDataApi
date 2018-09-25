# Generated by Django 2.1.1 on 2018-09-24 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20180918_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectrelation',
            name='from_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_relations', to='metadata.Object'),
        ),
        migrations.AlterField(
            model_name='objectrelation',
            name='to_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_relations', to='metadata.Object'),
        ),
    ]
