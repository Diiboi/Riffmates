# Generated by Django 5.2.1 on 2025-05-14 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='musician_profiles',
            field=models.ManyToManyField(blank=True, to='bands.musician'),
        ),
    ]
