# Generated by Django 4.2.9 on 2024-03-05 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('status', models.CharField(max_length=16)),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_phone_number', models.CharField(max_length=15)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='event.event')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoVenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/'),),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='venue.venue')),
            ],
        ),
    ]
