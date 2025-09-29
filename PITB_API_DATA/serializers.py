from rest_framework import serializers
from AppVehicle.models import VehicleData
from .models import PITBApiData

class PITBAPIDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PITBApiData
        fields = '__all__'

    