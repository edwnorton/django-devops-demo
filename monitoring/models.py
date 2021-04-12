from django.db import models
from rest_framework import serializers


class alerts(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    alertname = models.CharField(max_length=100, verbose_name='告警名称')
    instance = models.CharField(max_length=50, verbose_name='实例', blank=True)
    startsAt = models.DateTimeField(verbose_name='告警产生时间', blank=True)
    status = models.CharField(max_length=20, verbose_name='状态', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    message = models.CharField(max_length=500, verbose_name='告警信息', blank=True)
    endsAt = models.DateTimeField(verbose_name='告警结束时间', blank=True)
    callee = models.CharField(max_length=20, verbose_name='被叫号码', blank=True)
    callstatus = models.CharField(max_length=20, verbose_name='呼叫状态', blank=True)
    silentstatus = models.CharField(max_length=5, verbose_name='静默状态', blank=True)
    def __str__(self):
        return self.message

    class Meta:
        db_table = 'alerts'
        ordering = ['startsAt']  # 按故障时间倒排


class AlertsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = alerts
        fields = ('url', 'alertname', 'instance', 'startsAt', 'status',
                  'severity', 'message', 'endsAt', 'callee', 'callstatus', 'silentstatus', 'pk')


class alertsinf(models.Model):
    #id = models.CharField(max_length=10, primary_key=True)
    alertname = models.CharField(max_length=100, verbose_name='告警名称', blank=True)
    alerttype = models.CharField(max_length=20, verbose_name='告警类型', blank=True)
    group = models.CharField(max_length=20, verbose_name='告警组', blank=True)
    telgroup = models.CharField(max_length=20, verbose_name='告警通知组', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    def __str__(self):
        return self.alertname

    class Meta:
        db_table = 'alertsinf'


class AlertsinfSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = alertsinf
        fields = ('url', 'alertname', 'alerttype', 'group', 'telgroup', 'severity', 'pk')


class AlertGroup(models.Model):
    group = models.CharField(max_length=50)
    number = models.TextField()

    class Meta:
        db_table = 'AlertGroup'


class AlertGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AlertGroup
        fields = ('url', 'group', 'number', 'pk')





class SilenceInfo(models.Model):
    alertlevel = models.CharField(max_length=20)
    silencetime = models.CharField(max_length=20)

    class Meta:
        db_table = 'SilenceInfo'


class SilenceInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SilenceInfo
        fields = ('url', 'alertlevel', 'silencetime', 'pk')


