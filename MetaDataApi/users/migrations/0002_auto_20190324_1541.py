# Generated by Django 2.1.7 on 2019-03-24 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0003_auto_20190324_1156'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'default_related_name': 'profile'},
        ),
        migrations.AddField(
            model_name='profile',
            name='foaf_person',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='profile',
                                    to='metadata.ObjectInstance'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
