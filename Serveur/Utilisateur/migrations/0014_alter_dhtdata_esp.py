# Generated by Django 5.1 on 2024-09-21 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateur', '0013_dhtdata_esp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dhtdata',
            name='esp',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Utilisateur.esp'),
        ),
    ]
