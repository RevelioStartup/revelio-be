from django.db import migrations, models

def create_packages(apps, schema_editor):
    Package = apps.get_model('package', 'Package')
    Package.objects.create(
        name='Free',
        price=0,
        duration=0,
        event_planner=True,
        event_tracker=True,
        event_timeline=True,
        event_rundown=True,
        ai_assistant=False
    )
    Package.objects.create(
        name='Premium',
        price=10000,
        duration=30,
        event_planner=True,
        event_tracker=True,
        event_timeline=True,
        event_rundown=True,
        ai_assistant=True
    )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('event_planner', models.BooleanField(default=False)),
                ('event_tracker', models.BooleanField(default=False)),
                ('event_timeline', models.BooleanField(default=False)),
                ('event_rundown', models.BooleanField(default=False)),
                ('ai_assistant', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(create_packages),
    ]
