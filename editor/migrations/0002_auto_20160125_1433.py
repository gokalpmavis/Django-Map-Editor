# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingObject',
            fields=[
                ('ID', models.DecimalField(default=2805, serialize=False, primary_key=True, decimal_places=0, max_digits=8)),
                ('Name', models.CharField(max_length=200)),
                ('Creator', models.CharField(default=b'admin', max_length=30)),
                ('Location', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapObject',
            fields=[
                ('ID', models.DecimalField(default=1766, serialize=False, primary_key=True, decimal_places=0, max_digits=8)),
                ('Name', models.CharField(max_length=200)),
                ('Owner', models.CharField(default=b'admin', max_length=200)),
                ('Size', models.DecimalField(default=100, max_digits=3, decimal_places=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NaturalElementObject',
            fields=[
                ('ID', models.DecimalField(default=1118, serialize=False, primary_key=True, decimal_places=0, max_digits=8)),
                ('Name', models.CharField(max_length=200)),
                ('Creator', models.CharField(default=b'admin', max_length=30)),
                ('Location', models.CharField(max_length=200)),
                ('Type', models.CharField(max_length=20)),
                ('Map', models.ForeignKey(to='editor.MapObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoadObject',
            fields=[
                ('ID', models.DecimalField(default=1989, serialize=False, primary_key=True, decimal_places=0, max_digits=8)),
                ('Name', models.CharField(max_length=200)),
                ('Creator', models.CharField(default=b'admin', max_length=30)),
                ('Location', models.CharField(max_length=200)),
                ('Map', models.ForeignKey(to='editor.MapObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Map',
        ),
        migrations.AddField(
            model_name='buildingobject',
            name='Map',
            field=models.ForeignKey(to='editor.MapObject'),
            preserve_default=True,
        ),
    ]
