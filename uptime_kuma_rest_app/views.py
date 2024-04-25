from rest_framework import viewsets, status as rf_status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Monitor, Heartbeat, Status as StatusModel, Note
from .serializers import MonitorSerializer, HeartbeatSerializer, StatusSerializer, NoteSerializer

# Monitor viewset to handle CRUD operations for Monitor model
class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

# Heartbeat viewset to handle CRUD operations for Heartbeat model
class HeartbeatViewSet(viewsets.ModelViewSet):
    queryset = Heartbeat.objects.all()
    serializer_class = HeartbeatSerializer

# Status viewset to handle CRUD operations for Status model
class StatusViewSet(viewsets.ModelViewSet):
    queryset = StatusModel.objects.all()
    serializer_class = StatusSerializer

# Note viewset to handle CRUD operations for Note model
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

# API view to receive heartbeat data along with associated monitor data
@api_view(['POST'])
def receive_heartbeat(request):
    print("Headers:", request.headers)
    print("Body:", request.data)

    monitor_data = request.data.get('monitor')
    monitor_id = monitor_data.get('id')

    # Check if monitor exists, if not create one
    monitor, created = Monitor.objects.get_or_create(
        uptime_kuma_monitor_id=monitor_id,
        defaults={
            'name': monitor_data['name'],
            'url': monitor_data['url'],
            'monitor_type': monitor_data['type'],
            'interval': monitor_data['interval']
        }
    )

    # Process the heartbeat data
    heartbeat_data = request.data.get('heartbeat')
    status_text = heartbeat_data['status']
    status, _ = StatusModel.objects.get_or_create(status_text=status_text)

    heartbeat = Heartbeat(
        monitor=monitor,
        status=status,
        timestamp=heartbeat_data['timestamp'],
        error_message=heartbeat_data.get('error')
    )
    heartbeat.save()

    # Prepare the response message
    response_data = {
        "message": "Heartbeat received successfully",
        "monitor_created": created
    }
    return Response(response_data, status=rf_status.HTTP_201_CREATED)
