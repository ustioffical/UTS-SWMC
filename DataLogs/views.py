from django.shortcuts import render
from .models import APITransmissionData
from rest_framework import viewsets
from .serializers import APITransmissionDataSerializer
# Create your views here.
class DataLogsViewSet(viewsets.ModelViewSet):
    http_method_names = ['post','get']
    queryset = APITransmissionData.objects.all()
    serializer_class = APITransmissionDataSerializer