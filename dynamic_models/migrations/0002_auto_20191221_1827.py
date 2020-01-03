# Generated by Django 2.1.15 on 2019-12-21 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('external_id', models.TextField(blank=True, null=True)),
                ('start_date', models.TextField(blank=True, null=True)),
                ('start_date_local', models.TextField(blank=True, null=True)),
                ('timezone', models.TextField(blank=True, null=True)),
                ('start_latlng', models.TextField(blank=True, null=True)),
                ('end_latlng', models.TextField(blank=True, null=True)),
                ('location_country', models.TextField(blank=True, null=True)),
                ('visibility', models.TextField(blank=True, null=True)),
                ('upload_id_str', models.TextField(blank=True, null=True)),
                ('achievement_count', models.BigIntegerField(blank=True, null=True)),
                ('trainer', models.NullBooleanField()),
                ('commute', models.NullBooleanField()),
                ('manual', models.NullBooleanField()),
                ('heartrate_opt_out', models.NullBooleanField()),
                ('average_speed', models.FloatField(blank=True, null=True)),
                ('average_watts', models.FloatField(blank=True, null=True)),
                ('from_accepted_tag', models.NullBooleanField()),
                ('max_speed', models.FloatField(blank=True, null=True)),
                ('upload_id', models.BigIntegerField(blank=True, null=True)),
                ('start_latitude', models.FloatField(blank=True, null=True)),
                ('display_hide_heartrate_option', models.NullBooleanField()),
                ('kudos_count', models.BigIntegerField(blank=True, null=True)),
                ('elapsed_time', models.BigIntegerField(blank=True, null=True)),
                ('start_longitude', models.FloatField(blank=True, null=True)),
                ('average_heartrate', models.FloatField(blank=True, null=True)),
                ('photo_count', models.BigIntegerField(blank=True, null=True)),
                ('max_heartrate', models.FloatField(blank=True, null=True)),
                ('ÅÅÅ_id', models.BigIntegerField(blank=True, null=True)),
                ('private', models.NullBooleanField()),
                ('flagged', models.NullBooleanField()),
                ('elev_low', models.FloatField(blank=True, null=True)),
                ('device_watts', models.NullBooleanField()),
                ('total_elevation_gain', models.FloatField(blank=True, null=True)),
                ('elev_high', models.FloatField(blank=True, null=True)),
                ('has_heartrate', models.NullBooleanField()),
                ('moving_time', models.BigIntegerField(blank=True, null=True)),
                ('athlete_count', models.BigIntegerField(blank=True, null=True)),
                ('total_photo_count', models.BigIntegerField(blank=True, null=True)),
                ('kilojoules', models.FloatField(blank=True, null=True)),
                ('resource_state', models.BigIntegerField(blank=True, null=True)),
                ('comment_count', models.BigIntegerField(blank=True, null=True)),
                ('has_kudoed', models.NullBooleanField()),
                ('pr_count', models.BigIntegerField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('utc_offset', models.FloatField(blank=True, null=True)),
                ('average_cadence', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mutant_dynamic_models_activity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_state', models.BigIntegerField(blank=True, null=True)),
                ('ÅÅÅ_id', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mutant_dynamic_models_athlete',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_polyline', models.TextField(blank=True, null=True)),
                ('resource_state', models.BigIntegerField(blank=True, null=True)),
                ('ÅÅÅ_id', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mutant_dynamic_models_map',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='sleep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awake', models.BigIntegerField(blank=True, null=True)),
                ('bedtime_end', models.TextField(blank=True, null=True)),
                ('bedtime_end_delta', models.BigIntegerField(blank=True, null=True)),
                ('bedtime_start', models.TextField(blank=True, null=True)),
                ('bedtime_start_delta', models.BigIntegerField(blank=True, null=True)),
                ('breath_average', models.FloatField(blank=True, null=True)),
                ('deep', models.BigIntegerField(blank=True, null=True)),
                ('duration', models.BigIntegerField(blank=True, null=True)),
                ('efficiency', models.BigIntegerField(blank=True, null=True)),
                ('hr_5min', models.TextField(blank=True, null=True)),
                ('hr_average', models.FloatField(blank=True, null=True)),
                ('hr_lowest', models.BigIntegerField(blank=True, null=True)),
                ('hypnogram_5min', models.TextField(blank=True, null=True)),
                ('is_longest', models.BigIntegerField(blank=True, null=True)),
                ('light', models.BigIntegerField(blank=True, null=True)),
                ('midpoint_at_delta', models.BigIntegerField(blank=True, null=True)),
                ('midpoint_time', models.BigIntegerField(blank=True, null=True)),
                ('onset_latency', models.BigIntegerField(blank=True, null=True)),
                ('period_id', models.BigIntegerField(blank=True, null=True)),
                ('rem', models.BigIntegerField(blank=True, null=True)),
                ('restless', models.BigIntegerField(blank=True, null=True)),
                ('rmssd', models.BigIntegerField(blank=True, null=True)),
                ('rmssd_5min', models.TextField(blank=True, null=True)),
                ('score', models.BigIntegerField(blank=True, null=True)),
                ('score_alignment', models.BigIntegerField(blank=True, null=True)),
                ('score_deep', models.BigIntegerField(blank=True, null=True)),
                ('score_disturbances', models.BigIntegerField(blank=True, null=True)),
                ('score_efficiency', models.BigIntegerField(blank=True, null=True)),
                ('score_latency', models.BigIntegerField(blank=True, null=True)),
                ('score_rem', models.BigIntegerField(blank=True, null=True)),
                ('score_total', models.BigIntegerField(blank=True, null=True)),
                ('summary_date', models.TextField(blank=True, null=True)),
                ('temperature_delta', models.FloatField(blank=True, null=True)),
                ('temperature_deviation', models.FloatField(blank=True, null=True)),
                ('temperature_trend_deviation', models.FloatField(blank=True, null=True)),
                ('timezone', models.BigIntegerField(blank=True, null=True)),
                ('total', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mutant_dynamic_models_sleep',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='CreateRequest',
        ),
    ]