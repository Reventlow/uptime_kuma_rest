from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, MonitorGroup, Monitor, Status, Heartbeat, Note
from rest_framework.authtoken.models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'created']
    fields = ['user']
    ordering = ['-created']
    search_fields = ['user__username', 'key']


# Inline for UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'


# Extend existing User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')

    def get_phone_number(self, instance):
        return instance.profile.phone_number

    get_phone_number.short_description = 'Phone Number'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# MonitorGroup Admin
@admin.register(MonitorGroup)
class MonitorGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


# Monitor Admin
@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'monitor_type', 'interval', 'silenced', 'uptime_kuma_monitor_id',
                    'display_maintainers', 'display_supporters']
    list_filter = ['silenced', 'monitor_type', 'monitor_group']
    search_fields = ['name', 'url']

    def display_maintainers(self, obj):
        return ", ".join([user.username for user in obj.users_main_maintainers.all()])

    display_maintainers.short_description = 'Main Maintainers'

    def display_supporters(self, obj):
        return ", ".join([user.username for user in obj.users_main_supporters.all()])

    display_supporters.short_description = 'Main Supporters'


# Status Admin
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['status_text']


# Heartbeat Admin
@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ['monitor', 'status', 'timestamp', 'forced_down']
    list_filter = ['status', 'forced_down']
    search_fields = ['monitor__name', 'status__status_text']


# Note Admin
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['message', 'timestamp', 'user', 'heartbeat']
    list_filter = ['timestamp', 'user']
    search_fields = ['message', 'user__username', 'heartbeat__monitor__name']
