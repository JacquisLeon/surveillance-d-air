# Generated by Django 5.1 on 2024-10-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrateur', '0009_esp_latitude_esp_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default='user', max_length=20),
        ),
    ]
