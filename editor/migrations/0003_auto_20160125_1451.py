# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_auto_20160125_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingobject',
            name='ID',
            field=models.DecimalField(default=3371, serialize=False, primary_key=True, decimal_places=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='mapobject',
            name='ID',
            field=models.DecimalField(default=7712, serialize=False, primary_key=True, decimal_places=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='naturalelementobject',
            name='ID',
            field=models.DecimalField(default=2170, serialize=False, primary_key=True, decimal_places=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='roadobject',
            name='ID',
            field=models.DecimalField(default=3411, serialize=False, primary_key=True, decimal_places=0, max_digits=8),
        ),
    ]
