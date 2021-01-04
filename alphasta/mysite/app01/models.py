from django.db import models
# from __future__ import unicode_literals

# Create your models here.
class t_viid_system(models.Model):
    id = models.AutoField(100, primary_key=True) #Ö÷¼ü
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    deviceId = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    ipAddr = models.CharField(max_length=15)
    ipv6Addr = models.CharField(max_length=15, null=True)
    port = models.CharField(max_length=6)
    onlineStatus = models.SmallIntegerField(1)
    count = models.SmallIntegerField(11, null=True)
    opTime = models.DateTimeField(null=True)
    receiveAddr = models.CharField(max_length=100, null=True)
    subscribeDetail = models.CharField(max_length=50, null=True)
    type = models.SmallIntegerField(1)

class t_subscribe(models.Model):
    subscribeID = models.CharField(max_length=33, primary_key=True)
    title = models.CharField(max_length=256)
    subscribeDetail = models.CharField(max_length=256)
    resourceClass = models.SmallIntegerField(11)
    resourceURI = models.TextField()
    applicantName = models.CharField(max_length=50)
    applicantOrg = models.CharField(max_length=100)
    beginTime = models.DateTimeField()
    endTime = models.DateTimeField()
    receiveAddr = models.CharField(max_length=256)
    reportInterval = models.SmallIntegerField(11)
    reason = models.CharField(max_length=256)
    operateType = models.SmallIntegerField(11)
    subscribeStatus = models.SmallIntegerField(11)
    subscribeCancelOrg = models.CharField(max_length=100)
    subscribeCancelPerson = models.CharField(max_length=32)
    cancelTime = models.DateTimeField()
    cancelReason = models.CharField(max_length=64)
    resultImageDeclare = models.CharField(max_length=64)
    resultFeatureDeclare = models.CharField(max_length=10)
    type = models.BooleanField()
    viidSystemID = models.CharField(max_length=10)

