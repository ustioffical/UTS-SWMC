from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# router=DefaultRouter()
# router.register('post-vtms-data',views.VTMSDataViewSet)
# router.register('stop-point-bulk',views.StopPointBulkViewSet)
# router.register('post-vtms-bulk-data',views.PostVTMSBulkDataViewSet,basename='post-vtms-bulk')
urlpatterns = [
    #     path('',include(router.urls)),
]
