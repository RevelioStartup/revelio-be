
# Generated by Django 4.2.9 on 2024-05-06 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.package'),
        ),
    ]