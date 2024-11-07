# Generated by Django 5.1 on 2024-10-23 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrateur', '0010_userprofile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seuils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humMax', models.FloatField(null=True)),
                ('humMin', models.FloatField(null=True)),
                ('tempMax', models.FloatField(null=True)),
                ('tempMin', models.FloatField(null=True)),
                ('gazMax', models.FloatField(null=True)),
                ('gazMin', models.FloatField(null=True)),
            ],
        ),
    ]
