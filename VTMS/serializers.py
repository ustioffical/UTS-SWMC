import datetime
from .models import *
from rest_framework import serializers
from .tasks import *
import logging
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class BulkProcessingResponse(APIException):
    status_code = 202  # Accepted
    default_detail = 'Bulk processing started'

    def __init__(self, detail):
        self.detail = detail


class PostVTMSDataSerializer(serializers.ModelSerializer):
    # You will only enter vehicle_no when
    # you are sending single data else leave it empty
    vehicle_no = serializers.CharField(write_only=True, required=False)
    bulk_data = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = APIVTMSData
        fields = '__all__'

    def create(self, validated_data):
        # First we check if bulk data is provided
        bulk_data = validated_data.pop('bulk_data', None)
        if bulk_data:

            logger.info(f"Recevied bulk data: {len(bulk_data)} records")
            process_bulk_vtms_data.delay(bulk_data)
            logger.info(f"Bulk data processing started for {len(bulk_data)} records")
            message = f"Processing {len(bulk_data)} records in the background."
            raise BulkProcessingResponse({"message": message})

        else:
            # Handle single vehicle data
            code = "PTA-1"  # Code of API from PITB table
            vehicle_no = validated_data.pop('vehicle_no', None)

            instance = super().create(validated_data)

            extracted_data = {
                'latitude': instance.latitude,
                'longitude': instance.longitude,
                'speed': instance.speed,
                'distance': instance.distance,
                'timestamp': instance.timestamp.strftime(
                    '%Y-%m-%d %H:%M:%S') if instance.timestamp else datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'vehicle_status': instance.vehicle_status,
                'engine_status': instance.engine_status
            }
            type = "single"
            if vehicle_no:
                save_transmission_data_single.delay(type, vehicle_no, extracted_data, code, instance.id)
            return instance


class PostStopPointBulkSerializer(serializers.ModelSerializer):
    bulk_data = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = APIVTMSStopPointBulk
        fields = '__all__'

    def create(self, validated_data):
        bulk_data = validated_data.pop('bulk_data', None)
        code = "PTA-2"
        if bulk_data:
            logger.info(f"Recevied bulk data: {len(bulk_data)} records")
            process_stop_point_bulk_data.delay(bulk_data, code)
            logger.info(f"Bulk data processing started for {len(bulk_data)} records")
            message = f"Processing {len(bulk_data)} records in the background."
            raise BulkProcessingResponse({"message": message})


class VehicleCodeSerializer(serializers.Serializer):
    vehicle_code = serializers.CharField(max_length=255, required=True)
    time_stamp = serializers.DateTimeField(required=True)
