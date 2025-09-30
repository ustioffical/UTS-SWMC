from rest_framework import serializers
from .models import APITransmissionData
from AppVehicle.models import VehicleData
#from PTIB_A.models import PITBApiData

class APITransmissionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = APITransmissionData
        fields = '__all__'

    