# Generated by Django 4.2.9 on 2024-04-23 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('midtrans_id', models.CharField(db_index=True, max_length=1024, unique=True)),
                ('order_id', models.CharField(db_index=True, max_length=1024, unique=True)),
                ('price', models.BigIntegerField()),
                ('checkout_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField()),
                ('payment_method', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_channel', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_type', models.CharField(blank=True, max_length=30, null=True)),
                ('payment_destination', models.CharField(blank=True, max_length=1024, null=True)),
                ('transaction_details', models.TextField(blank=True, null=True)),
                ('paid_at_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CANCELLED', 'Cancelled'), ('PROCESSING', 'Processing'), ('SUCCESS', 'Success'), ('REFUND', 'Refund'), ('EXPIRED', 'Expired')], db_index=True, default='PENDING', max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-checkout_date'],
            },
        ),
    ]