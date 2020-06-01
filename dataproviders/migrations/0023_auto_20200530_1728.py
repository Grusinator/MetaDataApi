# Generated by Django 2.1.15 on 2020-05-30 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0022_auto_20200530_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='auth_type',
            field=models.CharField(choices=[('token', 'token'), ('oauth2', 'oauth2'), (None, None)], default=None,
                                   max_length=10),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='api_type',
            field=models.CharField(choices=[('rest', 'rest'), ('graphql', 'graphql')], default='rest', max_length=10),
        ),
    ]