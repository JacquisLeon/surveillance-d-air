# Generated by Django 5.1 on 2024-09-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrateur', '0005_esp_dhtdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='esp',
            name='esp_id',
            field=models.CharField(default=0, max_length=50, unique=True),
        ),
    ]