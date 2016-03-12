from django.db import models
import json


# Create your models here.

from django.utils import timezone
import datetime
import uuid


def randomGen():
    return int(str(uuid.uuid4().int)[:10])
#-------------------------------MAP------------------------------------#            

class MapObject(models.Model):
    ID = models.DecimalField(primary_key=True,decimal_places=0,default = randomGen(),max_digits=12)
    Name = models.CharField(max_length=200)
    Owner = models.CharField(max_length=200, default='admin')
    Size = models.DecimalField(decimal_places=0,default = 100,max_digits=3)
class BuildingObject(models.Model):
    Map = models.ForeignKey(MapObject)
    ID = models.DecimalField(primary_key=True,decimal_places=0,default = randomGen(),max_digits=12)
    Name = models.CharField(max_length=200)
    Creator = models.CharField(max_length=30, default='admin')
    Location = models.CharField(max_length=200)
    def getLocation(self):
        return json.loads(self.Location)
class NaturalElementObject(models.Model):  
    Map = models.ForeignKey(MapObject) 
    ID = models.DecimalField(primary_key=True,decimal_places=0,default = randomGen(),max_digits=12)
    Name = models.CharField(max_length=200)
    Creator = models.CharField(max_length=30, default='admin') 
    Location = models.CharField(max_length=200)
    Type = models.CharField(max_length=20 ,unique = False)
    
    def getLocation(self):
        return json.loads(self.Location)
class RoadObject(models.Model):   
    Map = models.ForeignKey(MapObject)
    ID = models.DecimalField(primary_key=True,decimal_places=0,default = randomGen(),max_digits=12)
    Name = models.CharField(max_length=200)
    Creator = models.CharField(max_length=30, default='admin')
    Location = models.CharField(max_length=200)

    def getLocation(self):
        return json.loads(self.Location)
    