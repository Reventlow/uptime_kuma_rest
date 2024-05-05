from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import MonitorViewSet, HeartbeatViewSet, StatusViewSet, NoteViewSet, receive_heartbeat, MonitorStatusView, MonitorStatusTemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import permissions

app_name = 'uptime_kuma_rest_app'

router = DefaultRouter()
router.register(r'monitors', MonitorViewSet)
router.register(r'heartbeats', HeartbeatViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Web views
    path('monitor-status/', MonitorStatusTemplateView.as_view(), name='monitor-status-view'),

    # API schema views
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/heartbeats/receive/', receive_heartbeat, name='receive-heartbeat'),  # Endpoint to receive heartbeat notifications
    #path('test-auth/', test_auth, name='test-auth'),  # Test authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Token authentication endpoint
    path('api/monitors/status/', MonitorStatusView.as_view(), name='monitor-status'),  # Monitor status endpoint
]

