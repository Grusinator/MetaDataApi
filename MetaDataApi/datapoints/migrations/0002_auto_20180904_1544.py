# Generated by Django 2.1 on 2018-09-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapointv2',
            name='std',
            field=models.FloatField(blank=True, null=True),
        ),
    ]