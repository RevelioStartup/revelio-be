# Generated by Django 4.2.9 on 2024-04-18 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rundown', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rundown',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
