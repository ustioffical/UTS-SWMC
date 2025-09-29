import datetime
from celery import shared_task
from .models import *
from AppVehicle.models import VehicleData
from DataLogs.models import APITransmissionData
from .models import APIVTMSData
import logging
import requests
import os
from django.shortcuts import get_object_or_404
from PITB_API_DATA.models import PITBApiData

AUTH_KEY = os.environ.get('AUTH_KEY')

logger = logging.getLogger(__name__)

@ shared_task
def process_bulk_vtms_data(bulk_data):
    code="PTA-1"
    processed_count=0
    type="bulk"
    for item in bulk_data:
        try:
                vehicle_no=item.pop('vehicle_no', None)
                instance=APIVTMSData.objects.create(**item)
                extracted_data={
                    'latitude': instance.latitude,
                    'longitude': instance.longitude,
                    'speed': instance.speed,
                    'distance': instance.distance,
                    'timestamp': instance.timestamp.strftime('%Y-%m-%d %H:%M:%S') if instance.timestamp else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'vehicle_status': instance.vehicle_status,
                    'engine_status': instance.engine_status
                }
                if vehicle_no:
                      save_transmission_data_single.delay(type,vehicle_no, extracted_data, code, instance.id)
                processed_count+=1
        except Exception as e:
                  logger.error(f"Error processing item {item}: {e}")

    logger.info(f"Processed {processed_count} items successfully out of {len(bulk_data)}")
    return processed_count

@shared_task
def save_transmission_data_single(type,vehicle_no, extracted_data, code,vtms_id):
    headers = {
        'Authorization': f'Bearer {AUTH_KEY}',
        'Content-Type': 'application/json'
    }
    if type=="single":
        api_url ="https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-data"
    else:
        api_url="https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-bulk-data"

    vehicle_code = get_object_or_404(VehicleData, vehicle_code=vehicle_no)
    pitb_api_code = get_object_or_404(PITBApiData, code=code)
    vtms_instance = get_object_or_404(APIVTMSData, id=vtms_id)

    response = requests.post(
            url=api_url,
            json=extracted_data,
            headers=headers
        )
    if response.status_code in [200, 201]:
        response_status = APITransmissionData.COMPLETED
    else:
        response_status = APITransmissionData.REJECTED

    # Get status code as string
    response_code = str(response.status_code)

    # Get response data
    remarks = str(response.json())

    # Create transmission record
    api_transmission = APITransmissionData.objects.create(
        pitb_api_code=pitb_api_code,
        vehicle_code=vehicle_code,
        response_code=response_code,
        response_status=response_status,
        remarks=remarks,
        created_by="Admin",
        updated_by="Admin"
    )
    # Update the VTMS instance with the transmission
    vtms_instance.tms_code = api_transmission
    vtms_instance.save()

    logger.info(f"Successfully processed VTMS ID {vtms_id}")


@shared_task
def process_stop_point_bulk_data(bulk_data,code):
    processed_count=0
    pitb_api_code = get_object_or_404(PITBApiData, code=code)

    for item in bulk_data:
        try:
            instance=APIVTMSStopPointBulk.objects.create(**item)

            extracted_data={
                'vehicle_code': instance.vehicle_code.vehicle_code if instance.vehicle_code else None,
                'gprs_raw_code': instance.gprs_raw_code.gprs_raw_code if instance.gprs_raw_code else None,
                'stopped_minutes': instance.stopped_minutes,
                'stopped_time': instance.stopped_time,
                'restart_time': instance.restart_time,
                'lat': instance.lat,
                'long': instance.long
            }
            headers = {
                'Authorization': f'Bearer {AUTH_KEY}',
                'Content-Type': 'application/json'
            }

            api_url="https://elgcd-ms.punjab.gov.pk/api/vtms/stop-points-bulk"

            response = requests.post(
                url=api_url,
                json=extracted_data,
                headers=headers
            )

            if response.status_code in [200, 201]:
                response_status = APITransmissionData.COMPLETED
            else:
                response_status = APITransmissionData.REJECTED

            # Get status code as string
            response_code = str(response.status_code)

            # Get response data
            remarks = str(response.json())

            api_transmission = APITransmissionData.objects.create(
            pitb_api_code=pitb_api_code,
            vehicle_code=instance.vehicle_code,
            response_code=response_code,
            response_status=response_status,
            remarks=remarks,
            created_by="Admin",
            updated_by="Admin"
        )

            instance.tms_code=api_transmission
            instance.save()
            processed_count+=1
            logger.info(f"Successfully processed VTMS ID {instance.id}")

        except Exception as e:
            logger.error(f"Error processing item {item}: {e}")

    logger.info(f"Processed {processed_count} items successfully out of {len(bulk_data)}")
