from django.db.models import OuterRef, Subquery, Exists, Q, Max
from rest_framework import viewsets, status as rf_status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.views.generic import TemplateView
from .models import Monitor, Heartbeat, Status as StatusModel, Note
from .serializers import MonitorSerializer, HeartbeatSerializer, StatusSerializer, NoteSerializer
from django.utils.timezone import now


# web views
class MonitorStatusTemplateView(TemplateView):
    template_name = 'monitors_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Using Subquery to get the last status and forced_down flag from Heartbeats
        last_heartbeat = Heartbeat.objects.filter(
            monitor=OuterRef('pk')
        ).order_by('-timestamp')

        monitors = Monitor.objects.annotate(
            last_status=Subquery(last_heartbeat.values('status__status_text')[:1]),
            last_forced_down=Subquery(last_heartbeat.values('forced_down')[:1])
        ).filter(
            ~Q(last_status='1'),
            last_forced_down=False
        )

        # Add the latest heartbeat and its notes to the monitor objects for context
        for monitor in monitors:
            latest_heartbeat = last_heartbeat.filter(monitor=monitor).first()
            monitor.latest_heartbeat = latest_heartbeat
            monitor.latest_notes = latest_heartbeat.notes.all() if latest_heartbeat else []

        context['monitors'] = monitors
        context['now'] = now()
        return context

# API views

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class HeartbeatViewSet(viewsets.ModelViewSet):
    queryset = Heartbeat.objects.all()
    serializer_class = HeartbeatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class StatusViewSet(viewsets.ModelViewSet):
    queryset = StatusModel.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

@extend_schema(
    methods=['get'],
    responses={200: MonitorSerializer(many=True)},
    description="Retrieves all monitors where the last heartbeat status is not '1' and not forced down, including the most recent heartbeat and all associated notes for each monitor."
)
class MonitorStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        monitors = Monitor.objects.annotate(
            last_status=Subquery(
                Monitor.heartbeats.filter(
                    monitor=OuterRef('pk')
                ).order_by('-timestamp').values('status__status_text')[:1]
            ),
            last_forced_down=Subquery(
                Monitor.heartbeats.filter(
                    monitor=OuterRef('pk')
                ).order_by('-timestamp').values('forced_down')[:1]
            )
        ).filter(
            last_status__ne='1',
            last_forced_down=False
        )

        serializer = MonitorSerializer(monitors, many=True)
        return Response(serializer.data)

@extend_schema(
    methods=['post'],
    request=HeartbeatSerializer,
    responses={201: HeartbeatSerializer},
    description="Processes a received heartbeat from Uptime Kuma, updates or creates monitor data accordingly."
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def receive_heartbeat(request):
    monitor_data = request.data.get('monitor')
    monitor_id = monitor_data.get('id')
    monitor, created = Monitor.objects.get_or_create(
        uptime_kuma_monitor_id=monitor_id,
        defaults={
            'name': monitor_data['name'],
            'url': monitor_data['url'],
            'monitor_type': monitor_data['type'],
            'interval': monitor_data['interval']
        }
    )
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
    response_data = HeartbeatSerializer(heartbeat).data
    return Response(response_data, status=rf_status.HTTP_201_CREATED)
