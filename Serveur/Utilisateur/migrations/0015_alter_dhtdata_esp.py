# Generated by Django 5.1 on 2024-09-21 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateur', '0014_alter_dhtdata_esp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dhtdata',
            name='esp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Utilisateur.esp'),
        ),
    ]