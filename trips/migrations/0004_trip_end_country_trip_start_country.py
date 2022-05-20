# Generated by Django 4.0.4 on 2022-05-15 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_alter_trip_passengers'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='end_country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='End_country', to='trips.country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='start_country',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='Start_country', to='trips.country'),
            preserve_default=False,
        ),
    ]