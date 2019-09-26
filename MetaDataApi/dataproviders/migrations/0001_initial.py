# Generated by Django 2.2.2 on 2019-09-26 18:06

import MetaDataApi.dataproviders.models.SerializableModel
import MetaDataApi.metadata.custom_storages
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.TextField(unique=True)),
                ('api_type', models.TextField(choices=[('OAUTH_REST', 'OauthRest'), ('OAUTH_GRAPHQL', 'OauthGraphql'), ('TOKEN_REST', 'TokenRest')], default='OauthRest')),
                ('api_endpoint', models.TextField()),
                ('data_provider_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='db_data_provider', to='metadata.Node')),
            ],
            bases=(models.Model, MetaDataApi.dataproviders.models.SerializableModel.SerializableModel),
        ),
        migrations.CreateModel(
            name='OauthConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorize_url', models.TextField()),
                ('access_token_url', models.TextField()),
                ('client_id', models.TextField()),
                ('client_secret', models.TextField()),
                ('scope', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('data_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='oauth_config', to='dataproviders.DataProvider')),
            ],
            bases=(models.Model, MetaDataApi.dataproviders.models.SerializableModel.SerializableModel),
        ),
        migrations.CreateModel(
            name='HttpConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('url_encoded_params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('body_type', models.TextField(blank=True, null=True)),
                ('body_content', models.TextField(blank=True, null=True)),
                ('request_type', models.TextField(blank=True, null=True)),
                ('data_provider', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='http_config', to='dataproviders.DataProvider')),
            ],
            bases=(models.Model, MetaDataApi.dataproviders.models.SerializableModel.SerializableModel),
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint_name', models.TextField()),
                ('endpoint_url', models.TextField()),
                ('request_type', models.TextField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE'), ('UPDATE', 'UPDATE')], default='GET')),
                ('data_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endpoints', to='dataproviders.DataProvider')),
            ],
            bases=(models.Model, MetaDataApi.dataproviders.models.SerializableModel.SerializableModel),
        ),
        migrations.CreateModel(
            name='DataDump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_downloaded', models.DateField(auto_now=True)),
                ('file', models.FileField(storage=MetaDataApi.metadata.custom_storages.PrivateMediaStorage(), upload_to='datafiles/')),
                ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_dumps', to='dataproviders.Endpoint')),
            ],
            bases=(models.Model, MetaDataApi.dataproviders.models.SerializableModel.SerializableModel),
        ),
    ]
