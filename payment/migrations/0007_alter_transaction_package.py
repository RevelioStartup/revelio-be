# Generated by Django 4.2.9 on 2024-05-06 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
        ('payment', '0006_remove_transaction_midtrans_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='package.package'),
        ),
    ]
