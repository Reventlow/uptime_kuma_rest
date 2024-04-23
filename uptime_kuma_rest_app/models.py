from django.db import models
from django.utils.translation import gettext_lazy as _

class Monitor(models.Model):
    """
    Model representing a monitor, which can have many heartbeats.
    """
    name = models.CharField(max_length=255, verbose_name=_("Monitor Name"))
    url = models.URLField(verbose_name=_("URL"))
    monitor_type = models.CharField(max_length=100, verbose_name=_("Type of Monitor"))
    uptime_kuma_monitor_id = models.IntegerField(verbose_name=_("Uptime Kuma Monitor ID"))
    interval = models.IntegerField(verbose_name=_("Interval in seconds"))

    def __str__(self):
        return self.name

class Status(models.Model):
    """
    Model representing the status of a heartbeat.
    """
    status_text = models.CharField(max_length=100, verbose_name=_("Status"))
    status_bootstrap_color = models.CharField(max_length=100, verbose_name=_("Status bootstrap color"))
    status_boostrap_button_text = models.CharField(max_length=100, verbose_name=_("Status boostrap button text"))

    def __str__(self):
        return self.status_text

class Heartbeat(models.Model):
    """
    Model representing a heartbeat, which belongs to a monitor and has a status.
    """
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='heartbeats', verbose_name=_("Monitor"))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, related_name='heartbeats', verbose_name=_("Status"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))
    error_message = models.TextField(blank=True, null=True, verbose_name=_("Error Message"))

    def __str__(self):
        return f"{self.monitor.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.status.status_text}"
