# Generated by Django 5.1 on 2024-09-27 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administrateur', '0006_esp_esp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='esp',
            name='esp_id',
        ),
    ]
