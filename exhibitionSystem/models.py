from __future__ import unicode_literals

from django.db import models

class user(models.Model):
    uid = models.CharField(max_length=10)

class boothInfo(models.Model):
    booth = models.CharField(max_length=30,default='')
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)
    info = models.TextField(max_length=300,default='')

class user_theme(models.Model):
    uid = models.CharField(max_length=10)
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)

class booth_conn(models.Model):
    B1 = models.CharField(max_length=30)
    B2 = models.CharField(max_length=30)

class user_booth(models.Model):
    uid = models.CharField(max_length=10)
    booth = models.CharField(max_length=30)
    reached = models.IntegerField(default=0)
    stayTime = models.IntegerField(default=0)

# Create your models here.
