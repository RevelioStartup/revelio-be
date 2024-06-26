# Generated by Django 4.2.9 on 2024-05-16 14:28

from django.db import migrations

from django.core.management import call_command


def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "package_feature.json") 

class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
