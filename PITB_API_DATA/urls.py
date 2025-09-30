from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from PITB_API_DATA.views import *

router = DefaultRouter()
router.register('', views.PITBAPIDATAViewset, basename='PITBApiData')

urlpatterns = [
    path('', include(router.urls)),
]
