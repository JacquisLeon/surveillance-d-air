# Generated by Django 5.1 on 2024-09-18 12:21

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateur', '0008_dhtdata_feux'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dhtdata',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dhtdata',
            name='gaz',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='dhtdata',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
