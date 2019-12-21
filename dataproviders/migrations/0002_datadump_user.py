# Generated by Django 2.1.15 on 2019-12-21 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dataproviders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datadump',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
