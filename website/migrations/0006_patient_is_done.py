# Generated by Django 5.0.7 on 2024-07-23 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_patient_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_done',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
