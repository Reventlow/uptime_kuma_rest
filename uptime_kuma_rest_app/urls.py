from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import MonitorViewSet, HeartbeatViewSet, StatusViewSet, NoteViewSet, test_auth, receive_heartbeat, MonitorStatusView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

app_name = 'uptime_kuma_rest_app'

router = DefaultRouter()
router.register(r'monitors', MonitorViewSet)
router.register(r'heartbeats', HeartbeatViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'notes', NoteViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Uptime Kuma API",
        default_version='v1',
        description="API for managing Uptime Kuma",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@localapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/heartbeats/receive/', receive_heartbeat, name='receive-heartbeat'),  # Endpoint to receive heartbeat notifications
    path('test-auth/', test_auth, name='test-auth'),  # Test authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Token authentication endpoint
    path('api/monitors/status_down/', MonitorStatusView.as_view(), name='monitor-status'),  # Monitor status_down endpoint
]
