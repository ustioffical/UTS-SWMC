from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('post-vtms-data',views.VTMSDataViewSet)
router.register('stop-point-bulk',views.StopPointBulkViewSet)
router.register('test-uts-single', views.UTSPostVTMSViewSet, basename='test-uts-single')
router.register('test-uts-loop', views.UTSPostVTMSLoopViewSet, basename='test-uts-loop')
#router.register('post-vtms-uts',views.UTSPostVTMSViewSet,basename='uts-vtms')
urlpatterns = [
    path('',include(router.urls)),
    #path('post-vehicle/', views.post_vehicle_data, name='post-vehicle-data'),
    #path('post-vehicle-loop/', views.post_vehicle_data_loop, name='post-vehicle-data-loop'),
]