# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_auto_20160125_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingobject',
            name='ID',
            field=models.DecimalField(default=2704405596, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='mapobject',
            name='ID',
            field=models.DecimalField(default=3046933178, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='naturalelementobject',
            name='ID',
            field=models.DecimalField(default=2077574011, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='roadobject',
            name='ID',
            field=models.DecimalField(default=4444570742, serialize=False, primary_key=True, decimal_places=0, max_digits=12),
        ),
    ]
