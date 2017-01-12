# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 11:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fifa_league', '0011_auto_20170112_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='players', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='player',
            name='photo',
            field=models.FileField(default='../static/fifa_league/gfx/player/default-player-photo.svg', upload_to='uploads/players/photo/'),
        ),
    ]
