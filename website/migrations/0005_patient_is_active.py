# Generated by Django 4.2.14 on 2024-07-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_alter_patient_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="is_active",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
