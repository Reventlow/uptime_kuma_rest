from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# User Profile Model for extending User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone Number"))

    def __str__(self):
        return self.user.username


# Signal to create or update User Profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


# Monitor Group Model
class MonitorGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Monitor Group Name"))

    def __str__(self):
        return self.name


# Monitor Model
class Monitor(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Monitor Name"))
    url = models.URLField(verbose_name=_("URL"), null=True, blank=True)
    github = models.URLField(verbose_name=_("GitHub URL"), blank=True, null=True)
    ops_url = models.URLField(verbose_name=_("OPS URL"), blank=True, null=True)
    monitor_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Type of Monitor"))
    interval = models.IntegerField(verbose_name=_("Interval in seconds"))
    silenced = models.BooleanField(default=False, verbose_name=_("Silenced"))
    monitor_group = models.ForeignKey(MonitorGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="monitors", verbose_name=_("Monitor Group"))
    uptime_kuma_monitor_id = models.IntegerField(verbose_name=_("Uptime Kuma Monitor ID"))
    users_main_maintainers = models.ManyToManyField(User, related_name='maintained_monitors', blank=True, verbose_name=_("Main Maintainers"))
    users_main_supporters = models.ManyToManyField(User, related_name='supported_monitors', blank=True, verbose_name=_("Main Supporters"))

    def __str__(self):
        return self.name


# Status Model
class Status(models.Model):
    status_text = models.CharField(max_length=100, verbose_name=_("Status"))

    def __str__(self):
        return self.status_text


# Heartbeat Model
class Heartbeat(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='heartbeats', verbose_name=_("Monitor"))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, related_name='heartbeats', verbose_name=_("Status"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))
    error_message = models.TextField(blank=True, null=True, verbose_name=_("Error Message"))
    forced_down = models.BooleanField(default=False, verbose_name=_("Forced Down"))
    assigned_users = models.ManyToManyField(User, related_name='heartbeats', verbose_name=_("Assigned Users"))

    def __str__(self):
        return f"{self.monitor.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.status.status_text}"


class Note(models.Model):
    message = models.TextField(verbose_name=_("Message"))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_("Timestamp"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes", verbose_name=_("Author"))
    heartbeat = models.ForeignKey(Heartbeat, on_delete=models.CASCADE, related_name='notes', verbose_name=_("Heartbeat"))

    def __str__(self):
        return f"Note by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


