from django.shortcuts import render
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# class VTMSDataViewSet(ModelViewSet):
#     http_method_names = ['post']
#     queryset = VTMSData.objects.all()
#     serializer_class = PostVTMSDataSerializer
#
# class StopPointBulkViewSet(ModelViewSet):
#     http_method_names = ['post']
#     queryset = StopPointBulk.objects.all()
#     serializer_class = PostStopPointBulkSerializer
#
# class PostVTMSBulkDataViewSet(ModelViewSet):
#     http_method_names = ['post']
#     queryset=VTMSData.objects.all()
#     serializer_class=PostVTMSBulkDataSerializer
