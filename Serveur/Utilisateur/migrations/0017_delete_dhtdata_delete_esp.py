# Generated by Django 5.1 on 2024-09-22 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateur', '0016_alter_dhtdata_esp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DHTData',
        ),
        migrations.DeleteModel(
            name='ESP',
        ),
    ]