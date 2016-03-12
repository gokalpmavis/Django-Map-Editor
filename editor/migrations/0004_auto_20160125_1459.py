# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_auto_20160125_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingobject',
            name='ID',
            field=models.DecimalField(default=3244558805, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='mapobject',
            name='ID',
            field=models.DecimalField(default=3245815398, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='naturalelementobject',
            name='ID',
            field=models.DecimalField(default=2728737515, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='roadobject',
            name='ID',
            field=models.DecimalField(default=3326749898, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
    ]
