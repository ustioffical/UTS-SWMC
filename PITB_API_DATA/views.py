from django.shortcuts import render
from .models import PITBApiData
from rest_framework import viewsets
from .serializers import PITBAPIDataSerializer


# Create your views here.
class PITBAPIDATAViewset(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'put', 'delete']
    queryset = PITBApiData.objects.all()
    serializer_class = PITBAPIDataSerializer

