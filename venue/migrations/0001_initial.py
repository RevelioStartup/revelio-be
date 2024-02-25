# Generated by Django 4.2.9 on 2024-02-25 02:58

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
                ('status', models.CharField(max_length=255)),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_phone_number', models.CharField(max_length=15)),
                ('event', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='venue_photos/')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='venue.venue')),
            ],
        ),
    ]