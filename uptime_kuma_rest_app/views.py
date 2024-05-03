from django.db.models import OuterRef, Subquery
from rest_framework import viewsets, status as rf_status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Monitor, Heartbeat, Status as StatusModel, Note
from .serializers import MonitorSerializer, HeartbeatSerializer, StatusSerializer, NoteSerializer

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

@swagger_auto_schema(
    method='post',
    operation_description="Receive a heartbeat from Uptime Kuma",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['heartbeat', 'monitor', 'msg'],
        properties={
            'heartbeat': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the heartbeat'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the heartbeat'),
                    'error': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description='Error message if any')
                }
            ),
            'monitor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the monitor'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the monitor'),
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the monitor'),
                    'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the monitor'),
                    'interval': openapi.Schema(type=openapi.TYPE_INTEGER, description='Monitoring interval in seconds')
                }
            ),
            'msg': openapi.Schema(type=openapi.TYPE_STRING, description='Message describing the heartbeat event')
        }
    ),
    responses={
        201: openapi.Response('Heartbeat processed successfully', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Confirmation message'),
                'monitor_created': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True if the monitor was created during this request')
            }
        )),
        400: openapi.Response('Invalid request'),
    }
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
    response_data = {
        "message": "Heartbeat received successfully",
        "monitor_created": created
    }
    return Response(response_data, status=rf_status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    operation_description="Test the authentication by returning the current user's information and the Authorization header received.",
    responses={
        200: openapi.Response('Authentication successful', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the authenticated user'),
                'received_header': openapi.Schema(type=openapi.TYPE_STRING, description='Authorization header received')
            }
        )),
        401: openapi.Response('Unauthorized', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message indicating failure of authentication')
            }
        ))
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_auth(request):
    return Response({
        "message": "You're authenticated!",
        "user": str(request.user),
        "received_header": request.headers.get('Authorization', 'No header found')
    })

@swagger_auto_schema(
    method='get',
    operation_summary="Get all monitors where the last heartbeat status is not '1' and not forced down",
    responses={200: MonitorSerializer(many=True)}
)
class MonitorStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_heartbeat = Heartbeat.objects.filter(
            monitor=OuterRef('pk')
        ).order_by('-timestamp').values('status__status_text', 'forced_down')[:1]

        monitors = Monitor.objects.annotate(
            last_status=Subquery(latest_heartbeat.values('status__status_text')),
            last_forced_down=Subquery(latest_heartbeat.values('forced_down'))
        ).filter(
            last_status__ne='1',
            last_forced_down=False
        )

        serializer = MonitorSerializer(monitors, many=True)
        return Response(serializer.data)
