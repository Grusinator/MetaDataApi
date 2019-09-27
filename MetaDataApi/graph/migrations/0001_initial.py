# Generated by Django 2.2.2 on 2019-09-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FieldSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('data_type', models.CharField(choices=[('character', 'character'), ('text', 'text'), ('integer', 'integer'), ('float', 'float'), ('boolean', 'boolean'), ('date', 'date')], editable=False, max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
