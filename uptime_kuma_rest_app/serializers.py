from rest_framework import serializers
from .models import Monitor, Heartbeat, Status, Note, MonitorGroup, User

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status_text']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MonitorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorGroup
        fields = ['id', 'name']

class MonitorSerializer(serializers.ModelSerializer):
    monitor_group = MonitorGroupSerializer(read_only=True)
    users_main_maintainers = UserSerializer(many=True, read_only=True)
    users_main_supporters = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Monitor
        fields = ['id', 'name', 'url', 'github', 'ops_url', 'monitor_type', 'interval', 'silenced', 'uptime_kuma_monitor_id', 'monitor_group', 'users_main_maintainers', 'users_main_supporters']

class HeartbeatSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    monitor = MonitorSerializer(read_only=True)
    assigned_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Heartbeat
        fields = ['monitor', 'status', 'timestamp', 'error_message', 'forced_down', 'assigned_users']

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    heartbeat = HeartbeatSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['message', 'timestamp', 'user', 'heartbeat']
