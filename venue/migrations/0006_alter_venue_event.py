# Generated by Django 4.2.9 on 2024-03-09 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_user'),
        ('venue', '0005_rename_photo_photovenue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='event.event'),
        ),
    ]
