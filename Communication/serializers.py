from .models import *
from rest_framework import serializers

# class PostVTMSDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=VTMSData
#         fields='__all__'
#
# class PostStopPointBulkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=StopPointBulk
#         fields='__all__'
#
#     def create(self,validated_data):
#         stop_point_bulk = [StopPointBulk(**item) for item in validated_data]
#         return StopPointBulk.objects.bulk_create(stop_point_bulk)
#
# class PostVTMSBulkDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=VTMSData
#         fields='__all__'
#
#     def create(self, validated_data):
#         vtms_data = [VTMSData(**item) for item in validated_data]
#         return VTMSData.objects.bulk_create(vtms_data)