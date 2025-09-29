import datetime
import os
import logging
import requests
from django.shortcuts import get_object_or_404
from .models import *
from rest_framework.serializers import ModelSerializer, Serializer, CharField, DateField
from AppVehicle.models import VehicleData
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from DataLogs.models import APITransmissionData
from PITB_API_DATA.models import PITBApiData

logger = logging.getLogger(__name__)
AUTH_KEY = os.environ.get('AUTH_KEY')


class ViewTripDataSerializer(ModelSerializer):
    pitb_code = CharField(source="vehicle_code.pitb_code", read_only=True)

    class Meta:
        model = APITripData
        fields = '__all__'


class PostTripDataSerializer(ModelSerializer):
    class Meta:
        model = APITripData
        fields = '__all__'

    def validate(self, attrs):
        # Validate that before_weight is greater than after_weight
        before_weight = attrs.get('before_weight')
        after_weight = attrs.get('after_weight')
        if before_weight <= after_weight:
            raise ValidationError({
                "before_weight": "Before weight must be greater than after weight."
            })

        # Validate that time_in is less than time_out
        time_in = attrs.get('time_in')
        time_out = attrs.get('time_out')
        if time_in >= time_out:
            raise serializers.ValidationError({
                "time_in": "Entry time must be earlier than exit time."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        trip_data = APITripData.objects.create(**validated_data)

        # Extract data from the created instance for API transmission
        extracted_data = {
            'vehicle_no': trip_data.vehicle_code,
            'before_weight': trip_data.before_weight,
            'after_weight': trip_data.after_weight,
            'time_in': trip_data.time_in.strftime('%Y-%m-%d %H:%M:%S') if hasattr(trip_data.time_in,
                                                                                  'strftime') else trip_data.time_in,
            'time_out': trip_data.time_out.strftime('%Y-%m-%d %H:%M:%S') if hasattr(trip_data.time_out,
                                                                                    'strftime') else trip_data.time_out,
            'before_picture': trip_data.before_picture,
            'after_picture': trip_data.after_picture,
            'roof_before_picture': trip_data.roof_before_picture,
            'roof_after_picture': trip_data.roof_after_picture,
            'uuid': trip_data.uuid,
            'slip_id': trip_data.slip_id,
            'data_id': trip_data.data_id,
            'lat': trip_data.lat,
            'long': trip_data.long,
            'site_name': trip_data.site_name,
            'site_id': trip_data.site_id
        }

        # Make API request
        try:
            headers = {
                "authkey": "SGWMC-xYzA9B3LmN7pQWVcJtK4RfEdGH2TsMUoZ68XYPbCvF5NDqhKJwL",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }

            api_url = "https://elgcd-ms.punjab.gov.pk/api/vtcs/post-trip-data"

            response = requests.post(
                url=api_url,
                data=extracted_data,
                headers=headers
            )

            # Determine response status
            if response.status_code in [200, 201]:
                response_status = APITransmissionData.COMPLETED
            else:
                response_status = APITransmissionData.REJECTED

            # Get status code as string
            response_code = str(response.status_code)

            # Get response data
            remarks = str(response.json())

            # Get vehicle and API code references
            vehicle_code = get_object_or_404(VehicleData, vehicle_code=trip_data.vehicle_code)
            pitb_api_code = get_object_or_404(PITBApiData, code="PTA-1")

            # Create transmission record
            tms_code_number = APITransmissionData.objects.count() + 1
            tms_code = f"TMS-{tms_code_number}"
            api_transmission = APITransmissionData.objects.create(
                tms_code=tms_code,
                pitb_api_code=pitb_api_code,
                vehicle_code=vehicle_code,
                response_code=response_code,
                response_status=response_status,
                remarks=remarks,
                created_by="Admin",
                updated_by="Admin"
            )

            # Update the trip data instance with the transmission
            trip_data.tms_code = api_transmission
            trip_data.save()

            logger.info(f"Successfully processed trip data ID {trip_data.id}")

        except Exception as e:
            logger.error(f"Error processing trip data {trip_data.id}: {e}")

        return trip_data, remarks
