from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uptime_kuma/', include('uptime_kuma_rest_app.urls', namespace='uptime_kuma_rest_app')),
    path('', RedirectView.as_view(pattern_name='uptime_kuma_rest_app:monitor-status-view'), name='home'),
    path('pages/', include('pages_app.urls', namespace='pages_app')),
    path('accounts/', include('authenticate_app.urls', namespace='authenticate_app')),
    #path('uptime_kuma/api/', include('uptime_kuma_rest_app.api_urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
