# Generated by Django 4.2.9 on 2024-02-26 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]