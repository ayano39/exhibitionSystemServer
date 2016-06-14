from __future__ import unicode_literals

from django.db import models

class user(models.Model):
    uid = models.AutoField(primary_key=True)
    frontdate = models.DateTimeField(default=0)
    frontboothid = models.IntegerField(default=0)

class boothInfo(models.Model):
    booth_id = models.AutoField(primary_key=True)
    booth = models.CharField(max_length=30, default='')
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)
    info = models.TextField(max_length=300, default='')

class user_theme(models.Model):
    uid = models.IntegerField()
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)

class booth_conn(models.Model):
    B1 = models.IntegerField(boothInfo)
    B2 = models.IntegerField(boothInfo)

class user_booth(models.Model):
    uid = models.IntegerField()
    booth_id = models.IntegerField()
    reached = models.IntegerField(default=0)

# Create your models here.
