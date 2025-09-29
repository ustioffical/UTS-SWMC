from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('logs',views.DataLogsViewSet)
urlpatterns = [
    path('',include(router.urls)),
]