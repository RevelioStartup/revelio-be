# Generated by Django 4.2.9 on 2024-05-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_usertoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='subscription_end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
