# Generated by Django 4.2.9 on 2024-03-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0003_alter_venue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]