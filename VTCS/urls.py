from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('post-trip-data',views.PostTripDataViewSet)
#router.register('post-to-pitb', views.VTCSPostToPITBViewSet, basename='post-to-pitb')
router.register('get-trip-data',views.ViewVTCSTripDataViewSet,basename='get-trip-data')
#router.register('update-trip-data',views.UpdateVTCSPITBAPIByIdViewSet,basename='update-trip-data')

urlpatterns = [
    path('',include(router.urls)),

    path('Pitb-Api/Trip-List/', views.ViewVTCSTripDataList, name='VTCSTripDataList'),
    path('Pitb-Api/TripData_Form/', views.PushVTCSTripData_FormView, name='PushVTCSTripData_Form'),
    # path('post-to-pitbpage/', views.post_vtcs_to_pitb_page, name='post_vtcs_to_pitb_page'),
    path('push-trip-data/', views.push_trip_data_view, name='push-trip-data'),
]