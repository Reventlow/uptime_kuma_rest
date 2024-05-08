from django.db.models import OuterRef, Subquery, Q, Prefetch
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.timezone import now
from rest_framework import viewsets, status as rf_status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Monitor, Heartbeat, Status as StatusModel, Note
from .serializers import MonitorSerializer, HeartbeatSerializer, StatusSerializer, NoteSerializer
import logging

logger = logging.getLogger(__name__)


# Web views
class MonitorStatusTemplateView(TemplateView):
    template_name = 'monitors_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_forced_down = Heartbeat.objects.filter(
            monitor=OuterRef('pk')
        ).order_by('-timestamp').values('forced_down')[:1]

        last_status_text = Heartbeat.objects.filter(
            monitor=OuterRef('pk')
        ).order_by('-timestamp').values('status__status_text')[:1]

        monitors = Monitor.objects.annotate(
            is_last_forced_down=Subquery(last_forced_down),
            last_status=Subquery(last_status_text)
        ).exclude(
            Q(last_status='up') & Q(is_last_forced_down=False)
        ).prefetch_related(
            Prefetch('heartbeats', queryset=Heartbeat.objects.order_by('-timestamp').prefetch_related('assigned_users'), to_attr='all_heartbeats')
        )

        for monitor in monitors:
            monitor.latest_heartbeat = monitor.all_heartbeats[0] if monitor.all_heartbeats else None

        context['monitors'] = monitors
        context['last_checked'] = now() if monitors else None
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
    description="Retrieves all monitors where the last heartbeat status is not 'up', and the latest heartbeat is not forced down, including the most recent heartbeat and all associated notes for each monitor."
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
            last_status__ne='up',
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


@require_POST
def toggle_forced_down(request, heartbeat_id):
    print(f"POST request handled by toggle_forced_down with ID: {heartbeat_id}")

    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    heartbeat = get_object_or_404(Heartbeat, id=heartbeat_id)
    heartbeat.forced_down = not heartbeat.forced_down
    heartbeat.save()
    return HttpResponse('solved', status=200)

