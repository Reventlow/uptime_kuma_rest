"""
URL configuration for uptime_kuma_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Uptime Kuma API",
      default_version='v1',
      description="API documentation for Uptime Kuma",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('uptime_kuma/', include('uptime_kuma_rest_app.urls', namespace='uptime_kuma_rest_app')),
    #path('', RedirectView.as_view(pattern_name='uptime_kuma_rest_app:list'), name='home'),
    path('pages/', include('pages_app.urls', namespace='pages_app')),
    path('accounts/', include('authenticate_app.urls',  namespace='authenticate_app')),
    #path('uptime_kuma/api/', include('uptime_kuma_rest_app.api_urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
