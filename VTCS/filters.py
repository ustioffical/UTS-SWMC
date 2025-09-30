from django_filters import rest_framework as filters
from .models import APITripData
from django.db import models

class APITripDataFilter(filters.FilterSet):
    vehicle_type = filters.CharFilter(field_name='vehicle_code__vehicle_type')
    start_date = filters.DateFilter(field_name='trip_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='trip_date', lookup_expr='lte')

    class Meta:
        model = APITripData
        fields = {
            'time_in': ['exact'],
            'time_out': ['exact'],
            'response_id': ['exact'],
            'response_status': ['exact'],
            'created_at': ['exact'],
            'site_name': ['exact'],
        }