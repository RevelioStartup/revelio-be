# Generated by Django 4.2.9 on 2024-03-03 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recommendationhistory",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
