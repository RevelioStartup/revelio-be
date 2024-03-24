# Generated by Django 4.2.9 on 2024-03-24 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task_steps', '0003_taskstep_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstep',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
