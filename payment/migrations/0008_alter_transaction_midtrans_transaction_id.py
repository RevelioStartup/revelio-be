# Generated by Django 4.2.9 on 2024-05-06 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_transaction_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='midtrans_transaction_id',
            field=models.CharField(db_index=True, default=None, max_length=1024, null=True, unique=True),
        ),
    ]
