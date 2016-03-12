# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0005_auto_20160125_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingobject',
            name='ID',
            field=models.DecimalField(default=1338940984, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='mapobject',
            name='ID',
            field=models.DecimalField(default=2684389460, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='naturalelementobject',
            name='ID',
            field=models.DecimalField(default=1715014263, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='roadobject',
            name='ID',
            field=models.DecimalField(default=2508928307, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
    ]
