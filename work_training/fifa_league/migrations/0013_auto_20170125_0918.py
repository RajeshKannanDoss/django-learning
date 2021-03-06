# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-25 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_league', '0012_auto_20170112_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'default_permissions': ('add', 'delete', 'change'), 'verbose_name': 'Team', 'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterField(
            model_name='player',
            name='photo',
            field=models.FileField(default='../static/fifa_league/gfx/player/default-player-photo.svg', upload_to='uploads/players/photos/'),
        ),
    ]
