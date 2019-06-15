# Generated by Django 2.2.2 on 2019-06-12 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dataproviders', '0010_auto_20190612_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataprovider',
            name='api_type',
            field=models.TextField(choices=[('OAUTH_REST', 'OAUTH_REST'), ('OAUTH_GRAPHQL', 'OAUTH_GRAPHQL'),
                                            ('TOKEN_REST', 'TOKEN_REST')], default='OauthRest'),
        ),
    ]