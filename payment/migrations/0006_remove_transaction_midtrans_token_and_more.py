# Generated by Django 4.2.9 on 2024-05-06 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
        ('payment', '0005_alter_transaction_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='midtrans_token',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='subscription',
        ),
        migrations.AddField(
            model_name='transaction',
            name='midtrans_url',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='package.package'),
        ),
    ]