# Generated by Django 5.1 on 2024-09-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateur', '0010_alter_dhtdata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ESP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu', models.CharField(max_length=100)),
            ],
        ),
    ]