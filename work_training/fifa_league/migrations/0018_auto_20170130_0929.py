# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-30 09:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_league', '0017_auto_20170127_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='shortcut',
        ),
        migrations.RemoveField(
            model_name='team',
            name='shortcut',
        ),
    ]