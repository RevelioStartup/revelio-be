# Generated by Django 4.2.9 on 2024-03-20 04:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStep',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('output', models.TextField()),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('ON_PROGRESS', 'ON_PROGRESS'), ('DONE', 'DONE')], default='NONE', max_length=16)),
                ('step_order', models.IntegerField()),
            ],
        ),
    ]
