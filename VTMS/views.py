from django.shortcuts import render
from .models import *
import json
from .serializers import *

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from AppVehicle.models import TrackerRawData, VehicleData, VehicleLiveMonitor
from rest_framework import status
from rest_framework.response import Response
import os
import datetime
import requests
import re

from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from geopy.distance import geodesic
from django.db.models import Max

import uuid

from django.utils.dateparse import parse_datetime
from django.utils import timezone


class VTMSDataViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = APIVTMSData.objects.all()
    serializer_class = PostVTMSDataSerializer


class StopPointBulkViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = APIVTMSStopPointBulk.objects.all()
    serializer_class = PostStopPointBulkSerializer


class VTMSDataViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = APIVTMSData.objects.all()
    serializer_class = PostVTMSDataSerializer


class StopPointBulkViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = APIVTMSStopPointBulk.objects.all()
    serializer_class = PostStopPointBulkSerializer


class UTSPostVTMSViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleCodeSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vehicle_code = serializer.validated_data['vehicle_code']
            time_stamp = serializer.validated_data['time_stamp'].strftime('%Y-%m-%d')
            result = UTSPostVTMS(vehicle_code, time_stamp)
            return Response(result, status=result.get('status', 200))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UTSPostVTMSLoopViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleCodeSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vehicle_code = serializer.validated_data['vehicle_code']
            time_stamp = serializer.validated_data['time_stamp'].strftime('%Y-%m-%d')
            result = UTSPostVTMSLoop(vehicle_code, time_stamp)
            return Response(result, status=result.get('status', 200))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Single
import json  # Add this import at the top with the other imports


def UTSPostVTMS(vehicle_code, str_selected_date):
    """
    Function to fetch and post vehicle tracker data to external VTMS API
    """
    try:
        try:
            vehicle = VehicleData.objects.get(vehicle_code=vehicle_code)
            get_pitb_vehicle_code = vehicle.vehicle_code
        except VehicleData.DoesNotExist:
            return {
                "error": f"Vehicle with code {vehicle_code} not found",
                "status": 404
            }

        dt_selected_date = datetime.datetime.strptime(str_selected_date, "%Y-%m-%d")
        # Get the latest tracker data for this vehicle
        datas = TrackerRawData.objects.filter(vehicle_code=vehicle,
                                              vendor_date_time__date=dt_selected_date,
                                              push_status="Pending").order_by('id')

        if not datas:
            return {
                "error": "No tracker data found for this vehicle",
                "status": 404
            }

        response_status_code = ""
        response_sync_code = ""
        response_text = ""
        response_count = 0
        # Process each data record in the loop
        for data in datas:

            # Extract 'Off' and 'On' as whole words
            status_match = re.findall(r'\b(Off|On)\b', data.device_status)
            set_engine_status = status_match[0] if status_match else "Off"

            # Make sure vehicle_status matches API requirements [moving/idle/waiting/still]
            set_vehicle_status = "moving"
            if data.device_status == "ACC Off,Parked":
                set_vehicle_status = "waiting"
            elif data.device_status == "ACC On,Idle":
                set_vehicle_status = "idle"

            # Format timestamp correctly
            format_str = '%Y-%m-%d %H:%M:%S'

            datetime_from_5_hour_str = (data.vendor_date_time + datetime.timedelta(hours=5)).strftime(format_str)
            dj_timestamp = datetime.datetime.strptime(datetime_from_5_hour_str, format_str)

            ### DATE CONVERT INTO STRING FORMAT
            work_date_str = dj_timestamp.strftime(format_str)
            timestamp = data.vendor_date_time.strftime(work_date_str)

            # Generate a 25-character UUID without hyphens
            short_uuid = uuid.uuid4().hex[:25]

            # Format data for the external API - ensuring proper format for all fields
            extracted_data = {
                "vehicle_no": str(get_pitb_vehicle_code),
                "uuid": short_uuid,  # Explicitly using 25-char hex UUID
                "lat": float(data.latitude),
                "long": float(data.longitude),
                "speed": float(data.speed),
                "distance": float(data.distance),
                "working_hour": 0,
                "timestamp": timestamp,
                "vehicle_status": set_vehicle_status,  # Must be one of: moving/idle/waiting/still
                "engine_status": set_engine_status.lower()  # Must be: on/off
            }

            # Log what we're about to send for debugging
            print(f"Sending data to API: {json.dumps(extracted_data)}")
            print(f"UUID length: {len(extracted_data['uuid'])}, value: {extracted_data['uuid']}")

            # Send data to external API with proper headers
            headers = {
                "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }

            api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-data"

            # Try with explicit JSON serialization
            response = requests.post(
                url=api_url,
                data=extracted_data,
                headers=headers,
                timeout=30
            )

            # Log the response for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")

            ### UPDATED TRACKER RAW DATA LATEST ROW

            response_status_code = response.status_code
            response_text = response.text
            response_count += 1

            json_str = response_text
            # Parse JSON string to dictionary
            json_data = json.loads(json_str)

            # Access data_id
            response_sync_code = str(json_data["data_id"])

            TrackerRawData.objects.filter(id=data.id).update(push_status='Completed', sync_code=response_sync_code)

        # Return the API response
        return {
            "status_code": response_status_code,
            "vehicle_data_count": response_count,
            "status": response_text,
            "message": response_text
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": 500
        }


def UTSPostVTMSLoop(vehicle_code, str_selected_date):
    """
    Function to fetch and post multiple vehicle tracker data points to external VTMS API
    """
    try:
        results = []  # Store results for each processed data entry

        try:
            vehicle = VehicleData.objects.get(vehicle_code=vehicle_code)
            get_pitb_vehicle_code = vehicle.pitb_code
        except VehicleData.DoesNotExist:
            return {
                "error": f"Vehicle with code {vehicle_code} not found",
                "status": 404
            }

        format_str = "%Y-%m-%d %H:%M:%S"

        dt_selected_date = datetime.datetime.strptime(str_selected_date, "%Y-%m-%d")
        # Get tracker data records for this vehicle on the selected date (limited to 10)
        datas = TrackerRawData.objects.filter(vehicle_code_id=vehicle, vendor_date_time__date=dt_selected_date)

        if not datas:
            return {
                "error": "No tracker data found for this vehicle on the selected date",
                "status": 404
            }

        # Process each data record in the loop
        for data in datas:
            try:
                # Extract 'Off' and 'On' as whole words
                status_match = re.findall(r'\b(Off|On)\b', data.device_status)
                set_engine_status = status_match[0] if status_match else "Off"

                # Make sure vehicle_status matches API requirements [moving/idle/waiting/still]
                set_vehicle_status = "moving"
                if data.device_status == "ACC Off,Parked":
                    set_vehicle_status = "waiting"
                elif data.device_status == "ACC On,Idle":
                    set_vehicle_status = "idle"

                # Format timestamp correctly
                # timestamp = data.vendor_date_time.strftime(
                #     '%Y-%m-%d %H:%M:%S') if data.vendor_date_time else datetime.datetime.now().strftime(
                #     '%Y-%m-%d %H:%M:%S')

                datetime_from_5_hour_str = (data.vendor_date_time + datetime.timedelta(hours=5)).strftime(format_str)
                dj_timestamp = datetime.datetime.strptime(datetime_from_5_hour_str, format_str)

                ### DATE CONVERT INTO STRING FORMAT
                work_date_str = dj_timestamp.strftime(format_str)
                timestamp = data.vendor_date_time.strftime(work_date_str)

                # Generate a 25-character UUID without hyphens
                short_uuid = uuid.uuid4().hex[:25]

                # Format data for the external API - ensuring proper format for all fields
                extracted_data = {
                    "vehicle_no": str(get_pitb_vehicle_code),
                    "uuid": short_uuid,  # Explicitly using 25-char hex UUID
                    "lat": float(data.latitude),
                    "long": float(data.longitude),
                    "speed": float(data.speed),
                    "distance": float(data.distance),
                    "working_hour": 0,
                    "timestamp": timestamp,
                    "vehicle_status": set_vehicle_status,  # Must be one of: moving/idle/waiting/still
                    "engine_status": set_engine_status.lower()  # Must be: on/off
                }

                # Log what we're about to send for debugging
                print(f"Sending data to API: {json.dumps(extracted_data)}")
                print(f"UUID length: {len(extracted_data['uuid'])}, value: {extracted_data['uuid']}")

                # Send data to external API with proper headers
                headers = {
                    "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }

                api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-data"

                # Try with explicit form data
                response = requests.post(
                    url=api_url,
                    data=extracted_data,
                    headers=headers,
                    timeout=30
                )

                # Log the response for debugging
                print(f"Response status: {response.status_code}")
                print(f"Response body: {response.text}")

                # Store the result for this entry
                results.append({
                    "status_code": response.status_code,
                    "response_data": response.json() if response.status_code in [200, 201] else response.text,
                    "vehicle_data": extracted_data
                })

            except Exception as inner_e:
                # Handle exceptions for individual records
                results.append({
                    "error": f"Error processing entry: {str(inner_e)}",
                    "vehicle_data": {
                        "vehicle_no": str(get_pitb_vehicle_code),
                        "timestamp": data.vendor_date_time.strftime(
                            '%Y-%m-%d %H:%M:%S') if data.vendor_date_time else None
                    }
                })

        # Return all results
        return {
            "results": results,
            "count": len(results),
            "status": 200
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": 500
        }


def UTSPostVTMSBulk(vehicle_code, str_selected_date):
    """
    Function to fetch and post multiple vehicle tracker data points to external VTMS API
    """
    data_to_send = []  # List to hold data to be sent in bulk

    try:

        try:
            vehicle = VehicleData.objects.get(vehicle_code=vehicle_code)
            get_pitb_vehicle_code = vehicle.pitb_code
        except VehicleData.DoesNotExist:
            return {
                "error": f"Vehicle with code {vehicle_code} not found",
                "status": 404
            }

        dt_selected_date = datetime.datetime.strptime(str_selected_date, "%Y-%m-%d")
        # Get tracker data records for this vehicle on the selected date (limited to 10)
        datas = TrackerRawData.objects.filter(vehicle_code_id=vehicle,
                                              vendor_date_time__date=dt_selected_date,
                                              push_status="Pending").order_by('id')

        if not datas:
            return {
                "error": "No tracker data found for this vehicle on the selected date",
                "status": 404
            }

        # Process each data record in the loop
        for data in datas:
            # Extract 'Off' and 'On' as whole words
            status_match = re.findall(r'\b(Off|On)\b', data.device_status)
            set_engine_status = status_match[0] if status_match else "Off"

            # Make sure vehicle_status matches API requirements [moving/idle/waiting/still]
            set_vehicle_status = "moving"
            if data.device_status == "ACC Off,Parked":
                set_vehicle_status = "waiting"
            elif data.device_status == "ACC On,Idle":
                set_vehicle_status = "idle"

            # Define the datetime format string
            format_str = '%Y-%m-%d %H:%M:%S'

            datetime_from_5_hour_str = (data.vendor_date_time + datetime.timedelta(hours=5)).strftime(format_str)
            dj_timestamp = datetime.datetime.strptime(datetime_from_5_hour_str, format_str)

            ### DATE CONVERT INTO STRING FORMAT
            work_date_str = dj_timestamp.strftime(format_str)
            timestamp = data.vendor_date_time.strftime(work_date_str)

            # Generate a 25-character UUID without hyphens
            short_uuid = uuid.uuid4().hex[:25]

            # Format data for the external API - ensuring proper format for all fields
            extracted_data = {
                "vehicle_no": (str(data.vehicle_code.pitb_code)).strip(),
                "uuid": short_uuid,  # Explicitly using 25-char hex UUID
                "lat": float(data.latitude),
                "long": float(data.longitude),
                "speed": float(data.speed),
                "distance": float(data.distance),
                "working_hour": 0,
                "timestamp": timestamp,
                "vehicle_status": set_vehicle_status,  # Must be one of: moving/idle/waiting/still
                "engine_status": set_engine_status.lower()  # Must be: on/off
            }
            data_to_send.append(extracted_data)

        if len(data_to_send) > 0:
            headers = {
                "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-bulk-data"

            # Try with explicit form data
            response = requests.post(
                url=api_url,
                json=data_to_send,
                headers=headers,
                timeout=30
            )

            # Log the response for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")

            ### UPDATED TRACKER RAW DATA LATEST ROW
            TrackerRawData.objects.filter(vehicle_code_id=vehicle,
                                          vendor_date_time__date=dt_selected_date,
                                          push_status="Pending").update(push_status='Completed')

            return {
                "api_response": {
                    "status_code": response.status_code,
                    "body": response.json() if response.status_code in [200, 201] else response.text
                },
                "data_sent": data_to_send,
                "count": len(data_to_send),
                "status": 200 if response.status_code in [200, 201] else response.status_code
            }

    except Exception as e:
        return {
            "error": str(e),
            "status": 500
        }


def UTSPostVTMSBulkBackend_2Min():
    """
    Function to fetch and post multiple vehicle tracker data points to external VTMS API
    """
    data_to_send = []  # List to hold data to be sent in bulk
    current_data_time = datetime.datetime.now()
    current_date = current_data_time.date()

    try:

        ###  GENERATE CODE IN WORKING SCHEDULE  ###
        GetVehicleLive = VehicleLiveMonitor.objects.all().order_by('vehicle_code_id')
        if len(GetVehicleLive) > 0:
            # Process each data record in the loop
            for data in GetVehicleLive:

                if data.vehicle_code.pitb_code is not None:

                    # Extract 'Off' and 'On' as whole words
                    status_match = re.findall(r'\b(Off|On)\b', data.device_status)
                    set_engine_status = status_match[0] if status_match else "Off"

                    # Make sure vehicle_status matches API requirements [moving/idle/waiting/still]
                    set_vehicle_status = "moving"
                    if data.device_status == "ACC Off,Parked":
                        set_vehicle_status = "waiting"
                    elif data.device_status == "ACC On,Idle":
                        set_vehicle_status = "idle"

                    # Define the datetime format string
                    timestamp = str(data.vendor_date_time)

                    # Generate a 25-character UUID without hyphens
                    short_uuid = uuid.uuid4().hex[:25]

                    ### CALCULATE VEHICLE DISTANCE
                    points = TrackerRawData.objects.filter(
                        vehicle_code_id=data.vehicle_code_id,
                        vendor_date_time__date=current_date
                    ).order_by('vendor_date_time').values('geom')

                    total_distance = 0.0
                    previous_point = None

                    for row in points:
                        point = GEOSGeometry(row['geom'])
                        if previous_point:
                            # geodesic needs (lat, lon)
                            dist = geodesic(
                                (previous_point.y, previous_point.x),
                                (point.y, point.x)
                            ).meters
                            total_distance += dist
                        previous_point = point
                    # print(f"Total distance (meters): {total_distance}")

                    # Format data for the external API - ensuring proper format for all fields
                    extracted_data = {
                        "vehicle_no": str(data.vehicle_code.pitb_code),
                        "uuid": short_uuid,  # Explicitly using 25-char hex UUID
                        "lat": float(data.latitude),
                        "long": float(data.longitude),
                        "speed": float(data.speed),
                        "distance": float(total_distance),
                        "working_hour": 0,
                        "timestamp": timestamp,
                        "vehicle_status": set_vehicle_status,  # Must be one of: moving/idle/waiting/still
                        "engine_status": set_engine_status.lower()  # Must be: on/off
                    }
                    data_to_send.append(extracted_data)

        if len(data_to_send) > 0:
            headers = {
                "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-bulk-data"

            # Try with explicit form data
            response = requests.post(
                url=api_url,
                json=data_to_send,
                headers=headers,
                timeout=30
            )

            # Log the response for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")

            ### UPDATED TRACKER RAW DATA LATEST ROW
            latest_ids = (
                TrackerRawData.objects
                .values('vehicle_code_id')
                .annotate(latest_id=Max('id'))
                .values_list('latest_id', flat=True)
            )
            TrackerRawData.objects.filter(id__in=latest_ids).update(push_status='Completed')

            return {
                "api_response": {
                    "status_code": response.status_code,
                    "body": response.json() if response.status_code in [200, 201] else response.text
                },
                "data_sent": data_to_send,
                "count": len(data_to_send),
                "status": 200 if response.status_code in [200, 201] else response.status_code
            }

    except Exception as e:
        return {
            "error": str(e),
            "status": 500
        }
