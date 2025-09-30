"""
URL configuration for LWMC_310 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('SWMC/', include('AppAccount.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('SWMC/', include('AppAdmin.urls')),
    path('SWMC/Map/', include('AppMapping.urls')),
    path('SWMC/Setting/', include('AppSetting.urls')),
    path('SWMC/Asset/', include('AppAsset.urls')),
    path('SWMC/Network/', include('AppRoute.urls')),
    path('SWMC/Vehicle/', include('AppVehicle.urls')),
    path('SWMC/Report/', include('AppReport.urls')),
    path('SWMC/VTMS/', include('VTMS.urls')),
    path('SWMC/VTCS/', include('VTCS.urls')),
    path('logs/', include('DataLogs.urls')),
    path('SWMC/Api/', include('PITB_API_DATA.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
