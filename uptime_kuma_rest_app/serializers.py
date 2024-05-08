from rest_framework import serializers
from .models import Monitor, Heartbeat, Status, Note, MonitorGroup, User
from drf_spectacular.utils import extend_schema_field, OpenApiExample

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

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['message', 'timestamp', 'user']

class HeartbeatSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    assigned_users = UserSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Heartbeat
        fields = ['id', 'status', 'timestamp', 'error_message', 'forced_down', 'assigned_users', 'notes']

@extend_schema_field(HeartbeatSerializer)
class LatestHeartbeatField(serializers.BaseSerializer):
    def to_representation(self, value):
        serializer = HeartbeatSerializer(value)
        return serializer.data

class MonitorSerializer(serializers.ModelSerializer):
    monitor_group = MonitorGroupSerializer(read_only=True)
    users_main_maintainers = UserSerializer(many=True, read_only=True)
    users_main_supporters = UserSerializer(many=True, read_only=True)
    latest_heartbeat = LatestHeartbeatField(source='get_latest_heartbeat', read_only=True)

    class Meta:
        model = Monitor
        fields = ['id', 'name', 'url', 'github', 'ops_url', 'monitor_type', 'interval', 'silenced', 'uptime_kuma_monitor_id', 'monitor_group', 'users_main_maintainers', 'users_main_supporters', 'latest_heartbeat']

    def get_latest_heartbeat(self, obj):
        return obj.heartbeats.order_by('-timestamp').first()
