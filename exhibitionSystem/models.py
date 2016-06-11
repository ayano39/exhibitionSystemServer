from __future__ import unicode_literals

from django.db import models

class user(models.Model):
    uid = models.CharField(max_length=10)

class boothInfo(models.Model):
    booth = models.CharField(max_length=30)
    coordx = models.IntegerField(default=0)
    coordy = models.IntegerField(default=0)
    info = models.TextField(max_length=300)

class user_theme(models.Model):
    uid = models.CharField(max_length=10)
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)

    def __str__(self):
        return self.uid

class booth_theme(models.Model):
    booth = models.CharField(max_length=30)
    medical = models.IntegerField(default=0)
    vehicle = models.IntegerField(default=0)
    home = models.IntegerField(default=0)
    industry = models.IntegerField(default=0)
    wear = models.IntegerField(default=0)


class user_booth(models.Model):
    uid = models.CharField(max_length=10)
    booth = models.CharField(max_length=30)
    reached = models.IntegerField(default=0)
    stayTime = models.IntegerField(default=0)

#hh
# Create your models here.
