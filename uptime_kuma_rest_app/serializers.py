from rest_framework import serializers
from .models import Monitor, Heartbeat, Status, Note

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status_text']

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id', 'name', 'url', 'monitor_type', 'interval']

class HeartbeatSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    class Meta:
        model = Heartbeat
        fields = ['status', 'timestamp', 'error_message']

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Note
        fields = ['message', 'timestamp', 'user']
