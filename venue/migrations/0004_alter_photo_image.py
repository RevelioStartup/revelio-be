# Generated by Django 4.2.9 on 2024-02-26 13:45

from django.db import migrations, models
import storages.backends.gcloud


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0003_alter_venue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(storage=storages.backends.gcloud.GoogleCloudStorage(), upload_to=''),
        ),
    ]
