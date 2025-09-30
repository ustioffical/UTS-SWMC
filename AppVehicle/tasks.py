import json

# from AppVehicle.views import GenerateWorkingWithVehicleSchedule_Function
# from VTMS.views import UTSPostVTMSBulkBackend_2Min
from django.shortcuts import render
from .models import *
from datetime import timedelta
from collections import defaultdict
from rest_framework import status
from rest_framework.response import Response
import os
import datetime
import requests
import re
from urllib.parse import urlencode
import pytz
import json
from django.utils.timezone import now
from django.utils import timezone

from django.contrib.gis.geos import GEOSGeometry
from django.db.models.expressions import RawSQL
from django.contrib.gis.db.models.functions import Length
from django.contrib.gis.db.models.aggregates import Collect, MakeLine

from geopy.distance import geodesic

from django.db.models import Max, Count

import uuid
import logging
from celery import shared_task
from django.utils.dateparse import parse_datetime

from AppAdmin.utils import AutoGenerateCodeForModel
from AppVehicle.models import TrackerRawData, VehicleData, VehicleLiveMonitor

logger = logging.getLogger(__name__)


# Step1
@shared_task
def GenerateWorkingWithVehicleSchedule_Function(selected_date):
    response_message = ""
    current_data_time = datetime.datetime.now()

    ### GENERATE VEHICLE SCHEDULA IN SYSTEM FUNCTION len(vehicle_list)
    vehicle_list = list(VehicleData.objects.filter(status="Active").order_by('vehicle_type'))
    ### IF CURRENT DATE EXIST OR NOT
    veh_sche_date_records = VehicleScheduleGPRSApi.objects.filter(veh_sch_date=selected_date)

    if len(vehicle_list) == len(veh_sche_date_records):
        response_message = "Equal Record"
        return response_message
    ### IF VEHICLE AND SCHEDULE VEHICLE EQUAL

    ### GENERATE WORKING SCHEDULA
    qs = WorkScheduleGPRSApi.objects.filter(work_date=selected_date)
    if not qs.exists():
        generated_code = AutoGenerateCodeForModel(WorkScheduleGPRSApi, "code", "WS-")
        new_record = WorkScheduleGPRSApi.objects.create(
            code=generated_code,
            work_date=selected_date,
            run_count=0,
            process_status="Pending",
            description="Sync-Current",
            created_at=current_data_time,
            created_by="admin"
        )
        ws_code = new_record.code
    else:
        existing = qs.first()
        ws_code = existing.code

    ### INSERTED ALL VEHICLE IN SCHEDULA MODEL
    for v in range(len(vehicle_list)):

        set_vehicle_code = vehicle_list[v].vehicle_code
        ### IF CURRENT DATE EXIST OR NOT
        current_date_records = VehicleScheduleGPRSApi.objects.filter(created_at=selected_date,
                                                                     vehicle_code_id=set_vehicle_code)
        if len(current_date_records) == 0:  ## IF CURRENT DATE EXIST
            response_message = "Created Record"
            gprs_code_number = VehicleScheduleGPRSApi.objects.count() + 1
            auto_vs_code = f"VAI-{gprs_code_number}"
            ### GPRS - VEHICLE SCHEDULE API (START)
            InstVehSche = VehicleScheduleGPRSApi(
                veh_api_code=auto_vs_code,
                vehicle_code_id=set_vehicle_code,
                veh_sch_date=selected_date,
                wsa_code_id=ws_code,
                retrieve_record=0,
                vendor_record=0,
                process_status="Pending",
                created_at=current_data_time,
                created_by="admin"
            )
            InstVehSche.save()
    #         ### GPRS - VEHICLE SCHEDULE API (END)
    #     ### NO RECORD FOUND CONDITION (END)
    # ### LOOP CONDITION (END)

    return response_message


# Step2:
@shared_task
def ResponseVehicleApi_By_Vendor_Function():
    ### Base URL
    base_url = "https://labs3.unitedtracker.com/api/UTS360/GetUserAllVehiclesDetailwithLocationbyUserCredentials"

    ### Define parameters ###
    params = {
        "UserName": "AKHTAR6792",
        "Password": "AKHTAR@6792",
        "VehicleID": 0,
        "isExcLocation": False,  # Current time
        "isExcTeltonikaLoc": False  # 30 seconds before current time
    }

    ### Generate URL with dynamic dates
    url = f"{base_url}?{urlencode(params)}"
    headers = {
        'API_KEY': '7b6f169d544e4eda4b2b263e6bffe50d',
        'Authorization': 'Basic UElUQjo4NTMwNWFlMjg1ZjVhNzk1OWY4OWE4YWY5Y2FhNWY1Nw=='
    }

    response_data = []
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()  # Get the response data from the external API
    except:
        print("error")

    dateTime = datetime.datetime.now()
    selected_date = dateTime.date()
    if len(response_data) > 0:  ### RECORD EXIST ###

        vehicle_response_api = response_data['MainData']
        for i in range(len(vehicle_response_api)):
            # CREATE AND UPDATE VEHICLE (START)
            ch_system_vehicle_id = vehicle_response_api[i]['VehicleId']

            VehicleStatus = VehicleData.objects.filter(vehicle_code=ch_system_vehicle_id)
            if len(VehicleStatus) > 0:  # UPDATE

                ck_vendor_date_time = str(vehicle_response_api[i]['GPSTime'])
                ck_system_date_time = vehicle_response_api[i]['RecTime']
                format_str = "%Y-%m-%d %H:%M:%S"
                try:
                    if '.' in ck_vendor_date_time:
                        ck_vendor_date_time = ck_vendor_date_time.split('.')[0]  # Remove the decimal part

                    _ck_vendor_date_time = datetime.datetime.fromisoformat(ck_vendor_date_time)
                    formatted_vendor_date_time = _ck_vendor_date_time.strftime(format_str)  # Format as a string
                    # print("Valid ISO format:")
                except ValueError:
                    # Parse into datetime object
                    formatted_vendor_date_time = datetime.strptime(ck_vendor_date_time, format_str)

                ### IF VEHICLE API DATE IS CURRENT DATE
                if _ck_vendor_date_time.date() == selected_date:

                    vt_latitude = vehicle_response_api[i]['Lat']
                    vt_longitude = vehicle_response_api[i]['Long']
                    get_feature_coordinate = "POINT(" + str(vt_longitude) + " " + str(vt_latitude) + ")"

                    ### GENERATE WORKING SCHEDULA
                    qs = VehicleLiveMonitor.objects.filter(vehicle_code_id=ch_system_vehicle_id)
                    if not qs.exists():
                        gprs_code_number = VehicleLiveMonitor.objects.count() + 1
                        auto_gprs_live_code = f"GPSL-{gprs_code_number}"
                        VehicleLiveMonitor.objects.create(
                            veh_live_mont_code=auto_gprs_live_code,
                            vehicle_code_id=ch_system_vehicle_id,
                            geom=get_feature_coordinate,
                            latitude=vt_latitude,
                            longitude=vt_longitude,
                            g_status=vehicle_response_api[i]['GStatus'],
                            speed=vehicle_response_api[i]['Speed'],
                            device_status=vehicle_response_api[i]['dev_status'],
                            direction=vehicle_response_api[i]['Direction'],
                            ignition_status=vehicle_response_api[i]['IgnStatus'],
                            geo_location=vehicle_response_api[i]['Location'],
                            vendor_date_time=formatted_vendor_date_time,
                            duration=vehicle_response_api[i]['Duration'],
                            created_at=dateTime,
                            created_by="admin"
                        )
                    else:
                        ### UPDATE LIVE MONITORING LOCATION START
                        VehicleLiveMonitor.objects.filter(vehicle_code_id=ch_system_vehicle_id).update(
                            geom=get_feature_coordinate,
                            latitude=vt_latitude,
                            longitude=vt_longitude,
                            g_status=vehicle_response_api[i]['GStatus'],
                            speed=vehicle_response_api[i]['Speed'],
                            device_status=vehicle_response_api[i]['dev_status'],
                            direction=vehicle_response_api[i]['Direction'],
                            ignition_status=vehicle_response_api[i]['IgnStatus'],
                            geo_location=vehicle_response_api[i]['Location'],
                            vendor_date_time=formatted_vendor_date_time,
                            duration=vehicle_response_api[i]['Duration'],
                            updated_at=dateTime,
                            updated_by="admin"
                        )
                        ### UPDATE LIVE MONITORING LOCATION START

                    ### TRACKER RAW DATA (START)
                    GetTrackerRawData = TrackerRawData.objects.filter(vehicle_code_id=ch_system_vehicle_id,
                                                                      vendor_date_time=ck_vendor_date_time)
                    if len(GetTrackerRawData) == 0:
                        gprs_code_number = int(
                            TrackerRawData.objects.order_by('-id').values_list('id', flat=True).first())
                        auto_gprs_code = f"GPRS-{gprs_code_number}"

                        InstTrackerRawData = TrackerRawData(
                            gprs_raw_code=auto_gprs_code,
                            vehicle_code_id=ch_system_vehicle_id,
                            terminal_no=vehicle_response_api[i]['TerminalNo'],
                            geom=get_feature_coordinate,
                            latitude=vt_latitude,
                            longitude=vt_longitude,
                            g_status=vehicle_response_api[i]['GStatus'],
                            vehicle_status=vehicle_response_api[i]['GStatus'],
                            device_status=vehicle_response_api[i]['dev_status'],
                            vendor_date_time=formatted_vendor_date_time,
                            system_date_time=ck_system_date_time,
                            speed=vehicle_response_api[i]['Speed'],
                            distance=vehicle_response_api[i]['Distance'],
                            direction=vehicle_response_api[i]['Direction'],
                            mileage=vehicle_response_api[i]['mileage_cur_value'],
                            push_status="Pending",
                            created_at=dateTime,
                            created_by="admin"
                        )
                        InstTrackerRawData.save()
                    # TRACKER RAW DATA (END)

            ### IF END (UPDATE)
        ### LOOP END
    ### STEP-2

    return response_data


# Step3

@shared_task
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

                    # Set up filters for today's data
                    tracker_filters = {
                        'vendor_date_time__date': current_date,
                        'vehicle_code_id': data.vehicle_code_id
                    }

                    # Get tracker records for this vehicle today
                    vehicle_tracker_records = TrackerRawData.objects.filter(**tracker_filters).order_by(
                        'vendor_date_time')
                    """
                    Calculate total distance (in km) for a vehicle on a given date.
                    Skips records without geometry.
                    """
                    total_distance = 0.0
                    previous_point = None

                    for row in vehicle_tracker_records:
                        point = GEOSGeometry(row.geom)
                        if previous_point:
                            # geodesic needs (lat, lon)
                            dist = geodesic(
                                (previous_point.y, previous_point.x),
                                (point.y, point.x)
                            ).meters
                            total_distance += dist
                        previous_point = point
                    # print(f"Total distance (meters): {total_distance}")

                    distance_km = (float(total_distance) / 1000)
                    round_distance_km = "{:.2f}".format(distance_km)
                    # print(f"Total distance (meters): {total_distance}")

                    """
                    Calculate total working (in hour) for a vehicle on a given date.
                    """
                    working_hours = 0
                    if vehicle_tracker_records.exists():
                        # Get all points with ACC On status
                        working_vehicles = []
                        for record in vehicle_tracker_records:
                            if record.device_status:
                                engine_status = record.device_status.strip().split(',')[0]
                                if engine_status == "ACC On":
                                    working_vehicles.append(record)

                        # Calculate working hours from ACC On points
                        if len(working_vehicles) >= 2:
                            for i in range(len(working_vehicles) - 1):  # Use working_vehicles, not all records
                                time_diff = (working_vehicles[i + 1].vendor_date_time - working_vehicles[
                                    i].vendor_date_time).total_seconds()
                                working_hours += time_diff / 3600  # Convert seconds to hours

                    # Format data for the external API - ensuring proper format for all fields
                    extracted_data = {
                        "vehicle_no": str(data.vehicle_code.pitb_code),
                        "uuid": short_uuid,  # Explicitly using 25-char hex UUID
                        "lat": float(data.latitude),
                        "long": float(data.longitude),
                        "speed": float(data.speed),
                        "distance": float(total_distance),
                        "working_hour": working_hours,
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


#  Missing vehicles code
@shared_task
def UTSPostVTMSBulkBackendMissingVehicles():
    format_str = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.datetime.now()

    # # Simple approach: Get local server time, fallback to Pakistan time
    # try:
    #     # Try to get local server time
    #     current_time = now()
    #     local_timezone_name = str(current_time.astimezone().tzinfo)
    #     logger.info(f"Using server local time: {local_timezone_name}")
    # except Exception as e:
    #     # Fallback to Pakistan time if local time fails
    #     logger.warning(f"Failed to get local server time, using Pakistan time: {e}")
    #
    #     pakistan_tz = pytz.timezone('Asia/Karachi')
    #     current_time = now().astimezone(pakistan_tz)
    #     logger.info("Using Pakistan Standard Time")

    current_date = current_time.date()
    # Calculate time 30 minutes earlier
    from_time = current_time - datetime.timedelta(minutes=10)

    # print(f"Current time: {current_time}")
    # print(f"10 minutes earlier: {from_time}")

    # Fetching data from vehicle live monitor using current_time_str and from_time_str
    # vehicle_live_data_list = list(VehicleLiveMonitor.objects.filter(
    #     vendor_date_time__lt=from_time  # CHANGE THIS LINE - Remove the ~Q wrapper
    # ))
    vehicle_live_data_list = list(VehicleLiveMonitor.objects.filter(
        vendor_date_time__lt=from_time  # CHANGE THIS LINE - Remove the ~Q wrapper
    ))

    # if len(vehicle_live_data_list) > 0:
    #     print(f"Found {len(vehicle_live_data_list)} vehicles with data outdated by more than 30 minutes")
    #     logger.info(f"Found {len(vehicle_live_data_list)} vehicles with data outdated by more than 30 minutes")

    # # Initialize these variables before any conditional blocks
    # latest_date = None
    # latest_longitude = None
    # latest_latitude = None
    # latest_record = None

    # Create a list to collect all data for bulk submission
    bulk_data_to_send = []

    # Track vehicle records to update after successful bulk submission
    vehicles_to_update = []

    # Now after getting the list of data from VehicleLiveMonitor we will run function
    ### GET VENDOR SERVER RESPONSE FROM TRACKER GPRS RAW DATA API FUNCTION
    for vehicle_live_data in vehicle_live_data_list:

        vehicle_id = vehicle_live_data.vehicle_code_id

        datetime_from = current_time - datetime.timedelta(minutes=10)
        api_datetime_from = datetime_from.strftime(format_str)
        api_datetime_to = current_time.strftime(format_str)
        # print(f"From time: {datetime_from} AND To time: {api_datetime_to}")

        ### INLINE TRACKER GPRS RAW API CALL - START ###
        # Base URL
        base_url = "https://labs3.unitedtracker.com/api/Trackers/GetVehicleHistoryByUserName"

        # Define parameters
        params = {
            "UserName": "AKHTAR6792",
            "Password": "AKHTAR@6792",
            "VehicleID": vehicle_id,
            "fromDate": api_datetime_from,
            "toDate": api_datetime_to
        }
        print(f"Define parameters: {params} ")

        # Generate URL with dynamic dates
        url = f"{base_url}?{urlencode(params)}"
        headers = {
            'API_KEY': '7b6f169d544e4eda4b2b263e6bffe50d',
            'Authorization': 'Basic UElUQjo4NTMwNWFlMjg1ZjVhNzk1OWY4OWE4YWY5Y2FhNWY1Nw=='
        }

        response_data = []
        response_message = ""
        try:
            logger.info(
                f"Requesting tracking data: VehicleID={vehicle_id}, from={api_datetime_from}, to={api_datetime_to}")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                response_message = "Data fetched successfully"

                # Safely log the first record if it exists
                if isinstance(response_data, dict) and 'Table' in response_data and response_data['Table']:
                    logger.info(f"First record: {json.dumps(response_data['Table'][0], indent=2)}")
                else:
                    logger.warning(
                        f"Response received but no records found in Table. Response: {str(response_data)[:200]}...")
            else:
                response_message = f"Data Not Fetch - Status code: {response.status_code}"
                logger.error(f"API request failed with status {response.status_code}: {response.text[:200]}")
        except Exception as e:
            response_message = f"Error: {str(e)}"
            logger.error(f"Exception when calling API: {str(e)}")
            # Return empty dict with Table key to prevent further errors
            response_data = {"Table": []}
        ### INLINE TRACKER GPRS RAW API CALL - END ###

        # Now finding the data from response_data with latest date
        records = None
        if response_data:
            records = response_data.get('Table', [])
            latest_record = None
            if records:
                latest_record = max(records, key=lambda r: r.get('GpsTime'))
                logger.info("Latest GpsTime record for %s: %s",
                            vehicle_id, json.dumps(latest_record))

                # Extract the needed values from the latest record
                latest_date = latest_record.get('GpsTime')
                latest_longitude = latest_record.get('Long')
                latest_latitude = latest_record.get('Lat')
                get_feature_coordinate = "POINT(" + str(latest_longitude) + " " + str(latest_latitude) + ")"

                VehicleLiveMonitor.objects.filter(vehicle_code=vehicle_id, vendor_date_time=datetime_from).update(
                    geom=get_feature_coordinate,
                    vendor_date_time=latest_date,
                    longitude=latest_longitude,
                    latitude=latest_latitude,

                )

                #             #     # g_status=vehicle_response_api[i]['GStatus'],
                #             #     # speed=vehicle_response_api[i]['Speed'],
                #             #     # device_status=vehicle_response_api[i]['dev_status'],
                #             #     # direction=vehicle_response_api[i]['Direction'],
                #             #     # ignition_status=vehicle_response_api[i]['IgnStatus'],
                #             #     # geo_location=vehicle_response_api[i]['Location'],
                #             #     # vendor_date_time=formatted_vendor_date_time,
                #             #     # duration=vehicle_response_api[i]['Duration'],
                #             #     # updated_at=dateTime,
                #             #     # updated_by="admin"


            else:
                logger.warning(
                    "No GPRS records for vehicle %s between %s and %s",
                    vehicle_id, api_datetime_from, api_datetime_to
                )

        #         # Now updating the vehicle live monitor
        #         if records and latest_date and latest_longitude and latest_latitude:
        #             ### UPDATE LIVE MONITORING LOCATION START
        #             # VehicleLiveMonitor.objects.filter(vehicle_code_id=ch_system_vehicle_id).update(
        #             #     # geom=get_feature_coordinate,
        #             #     # latitude=vt_latitude,
        #             #     # longitude=vt_longitude,
        #             #     # g_status=vehicle_response_api[i]['GStatus'],
        #             #     # speed=vehicle_response_api[i]['Speed'],
        #             #     # device_status=vehicle_response_api[i]['dev_status'],
        #             #     # direction=vehicle_response_api[i]['Direction'],
        #             #     # ignition_status=vehicle_response_api[i]['IgnStatus'],
        #             #     # geo_location=vehicle_response_api[i]['Location'],
        #             #     # vendor_date_time=formatted_vendor_date_time,
        #             #     # duration=vehicle_response_api[i]['Duration'],
        #             #     # updated_at=dateTime,
        #             #     # updated_by="admin"
        #             # )
        #             ### UPDATE LIVE MONITORING LOCATION START
        #
        #             VehicleLiveMonitor.objects.filter(vehicle_code=vehicle_id, vendor_date_time=datetime_from).update(
        #                 geom=get_feature_coordinate,
        #                 vendor_date_time=latest_date,
        #                 longitude=latest_longitude,
        #                 latitude=latest_latitude
        #             )
        #             auto_gprs_code = AutoGenerateCodeForModel(TrackerRawData, "gprs_raw_code", "GPRS-")
        #
        #             # Now inserting in Tracker Raw Data
        #             TrackerRawData.objects.create(
        #                 gprs_raw_code=auto_gprs_code,
        #                 vehicle_code=vehicle_id,
        #                 terminal_no=latest_record.get('TerminalNo'),
        #                 geom=f"POINT({latest_longitude} {latest_latitude})",
        #                 latitude=latest_latitude,
        #                 longitude=latest_longitude,
        #                 g_status=latest_record.get('Veh_Status', ''),
        #                 vehicle_status=latest_record.get('Veh_Status', ''),
        #                 device_status=latest_record.get('Dev_status', ''),
        #                 vendor_date_time=latest_record.get('GpsTime'),
        #                 system_date_time=latest_record.get('RecTime'),
        #                 speed=latest_record.get('Speed', 0.0),
        #                 distance=latest_record.get('Distance', 0.0),
        #                 direction=latest_record.get('Direction', 0.0),
        #                 mileage=latest_record.get('Mileage_Val', 0.0),
        #                 push_status="Pending",
        #                 created_at=now(),
        #                 created_by="admin"
        #             )
        #
        #             # # ****************************
        #             # # Calculate working hours using the same procedure as UTSPostVTMSBulkBackend_2Min
        #             # vehicle_tracker_records = TrackerRawData.objects.filter(
        #             #     vehicle_code_id=vehicle_id,
        #             #     vendor_date_time__date=current_date
        #             # ).order_by('vendor_date_time')
        #             #
        #             # working_hours = 0
        #             # if vehicle_tracker_records.exists():
        #             #     # Get all points with ACC On status
        #             #     working_vehicles = []
        #             #     for record in vehicle_tracker_records:
        #             #         if record.device_status:
        #             #             engine_status = record.device_status.strip().split(',')[0]
        #             #             if engine_status == "ACC On":
        #             #                 working_vehicles.append(record)
        #             #
        #             #     # Calculate working hours from ACC On points
        #             #     if len(working_vehicles) >= 2:
        #             #         for i in range(len(working_vehicles) - 1):  # Use working_vehicles, not all records
        #             #             time_diff = (working_vehicles[i + 1].vendor_date_time - working_vehicles[
        #             #                 i].vendor_date_time).total_seconds()
        #             #             working_hours += time_diff / 3600  # Convert seconds to hours
        #             # # *****************************
        #
        #             # # Prepare data for PITB API (bulk)
        #             # logger.info("Preparing data for PITB API bulk submission")
        #             # vehicle_pitb = VehicleData.objects.filter(vehicle_code=vehicle_id).values('pitb_code').first()
        #             # if not vehicle_pitb or not vehicle_pitb.get('pitb_code'):
        #             #     logger.warning(f"No PITB code found for vehicle {vehicle_id}, skipping...")
        #             #     continue
        #             # status_match = re.findall(r'\b(Off|On)\b', latest_record.get('Dev_status', ''))
        #             # set_engine_status = status_match[0] if status_match else "Off"
        #             #
        #             # # Determine vehicle status for PITB API
        #             # set_vehicle_status = "moving"
        #             # if "ACC Off,Parked" in latest_record.get('Dev_status', ''):
        #             #     set_vehicle_status = "waiting"
        #             # elif "ACC On,Idle" in latest_record.get('Dev_status', ''):
        #             #     set_vehicle_status = "idle"
        #             #
        #             # # Generate a unique identifier for this record
        #             # short_uuid = uuid.uuid4().hex[:25]
        #             #
                    # # Prepare data for this vehicle
                    # vehicle_data = {
                    #     "vehicle_no": str(vehicle_pitb['pitb_code']),
                    #     "uuid": short_uuid,
                    #     "lat": float(latest_latitude),
                    #     "long": float(latest_longitude),
                    #     "speed": float(latest_record.get('Speed', 0.0)),
                    #     "distance": float(latest_record.get('Distance', 0.0)),
                    #     "working_hour": working_hours,
                    #     "timestamp": str(latest_record.get('GpsTime')),
                    #     "vehicle_status": set_vehicle_status,
                    #     "engine_status": set_engine_status.lower()
                    # }
                    #
                    # # Add this vehicle's data to the bulk list
                    # bulk_data_to_send.append(vehicle_data)
                    #
                    # # Keep track of vehicles to update status after API call
                    # vehicles_to_update.append({
                    #     'vehicle_id': vehicle_id,
                    #     'timestamp': latest_record.get('GpsTime')
                    # })
        #
        else:
            logger.info("There might be some problem with the GPRS API response")
            print("There might be some problem with the GPRS API response")
    #
    # # # Send bulk data to PITB API if we have data to send
    # if bulk_data_to_send:
    #     logger.info(f"Sending {len(bulk_data_to_send)} vehicle records to PITB bulk API")
    #
    #     headers = {
    #         "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
    #         "Content-Type": "application/json",
    #         "Accept": "application/json"
    #     }
    #
    #     # Use the bulk API endpoint
    #     api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-bulk-data"
    #
    #     try:
    #         # Send the bulk request
    #         response = requests.post(
    #             url=api_url,
    #             json=bulk_data_to_send,
    #             headers=headers,
    #             timeout=30
    #         )
    #
    #         print(f"Bulk API response status: {response.status_code}")
    #         print(f"Bulk API response body: {response.text}")
    #         logger.info(f"Bulk API response status: {response.status_code}")
    #         logger.info(f"Bulk API response body: {response.text}")
    #
    #         # If the API call was successful, update all the vehicle records
    #         if response.status_code in [200, 201]:
    #             for vehicle in vehicles_to_update:
    #                 TrackerRawData.objects.filter(
    #                     vehicle_code=vehicle['vehicle_id'],
    #                     vendor_date_time=vehicle['timestamp']
    #                 ).update(push_status="Completed")
    #
    #             logger.info(f"Updated push_status to Completed for {len(vehicles_to_update)} vehicles")
    #
    #             return {
    #                 "message": f"Successfully sent {len(bulk_data_to_send)} vehicle records in bulk",
    #                 "status": 200,
    #                 "api_status": response.status_code
    #             }
    #         else:
    #             logger.error(f"Failed to send bulk data. Status code: {response.status_code}")
    #             return {
    #                 "error": f"Failed to send bulk data. Status code: {response.status_code}",
    #                 "status": 500,
    #                 "api_status": response.status_code
    #             }
    #
    #     except Exception as e:
    #         logger.error(f"Error during bulk API call: {str(e)}")
    #         return {
    #             "error": str(e),
    #             "status": 500
    #         }
    # else:
    #     logger.info("No data to send to PITB API")
    #     return {
    #         "message": "No data to send",
    #         "status": 200
    #     }


@shared_task
def UTSPostVTMSBulkBackgroundTask():
    step_competed = 0
    try:
        logger.info("Starting Step 1: Generating working schedule")
        current_date = datetime.datetime.now().date()
        step1 = GenerateWorkingWithVehicleSchedule_Function(current_date)
        step_competed += 1
        logger.info(f"Step 1 completed")
        logger.info("Starting Step 2: Fetching vehicle data from vendor")
        step2 = ResponseVehicleApi_By_Vendor_Function()
        step_competed += 1
        # logger.info(f"Step 2 completed")
        # step3 = UTSPostVTMSBulkBackend_2Min()
        # step_competed += 1
        # logger.info(f"Step 3 completed")

        step4 = UTSPostVTMSBulkBackendMissingVehicles()
        step_competed += 1
        logger.info(f"Step 4 Missing Vehicle")

    except Exception as e:
        logger.error(f"Error in UTSPostVTMSBulkBackgroundTask: {e}")
        return {
            "error": str(e),
            "status": 500,
            "step_completed": step_competed
        }

    return step_competed


# @shared_task
# def UTSPostVTMSPostData_local_database_single_vehicle(vehicle_code: str, selected_date: str):
#     format_str_date = "%Y-%m-%d"
#     format_str_date_time = "%Y-%m-%d %H:%M:%S"
#     current_data_time = datetime.datetime.now()
#     current_data = current_data_time.date()
#
#     ### CHECK VEHICLE VENDOR RECORD EQUAL TO DUMP RECORD WITH STATUS
#     fetch_vehicle_sche_record = VehicleScheduleGPRSApi.objects.get(veh_sch_date=selected_date,
#                                                                    vehicle_code_id=vehicle_code)
#     ck_process_status = fetch_vehicle_sche_record.process_status
#
#     if ck_process_status == "Pending":  ### PROCESS STATUS "PENDING" ###
#         ### CHECK VEHICLE GPRS LIST (START)
#
#         start_of_day_time_str = '00:00:00'
#         end_of_day_time_str = '23:59:59'
#         ### DATE CONVERT INTO STRING FORMAT
#         work_date_str = selected_date
#
#         ### COMBINE DATE AND TIME INTO STRING
#         datetime_from = work_date_str + " " + start_of_day_time_str  ## "2025-02-27 00:00:00"
#         datetime_to = work_date_str + " " + end_of_day_time_str  ## "2025-02-27 23:59:59"
#
#         ### GET VENDOR SERVER RESPONSE FROM TRACKER GPRS RAW DATA API FUNCTION
#
#         ### Base URL
#         base_url = "https://labs3.unitedtracker.com/api/Trackers/GetVehicleHistoryByUserName"
#
#         ### Define parameters ###
#         params = {
#             "UserName": "AKHTAR6792",
#             "Password": "AKHTAR@6792",
#             "VehicleID": vehicle_code,
#             "fromDate": datetime_from,  # 2025-04-15 14:00:02
#             "toDate": datetime_to  # toDate=2025-04-15 14:10:02
#         }
#
#         ### Generate URL with dynamic dates
#         url = f"{base_url}?{urlencode(params)}"
#         headers = {
#             'API_KEY': '7b6f169d544e4eda4b2b263e6bffe50d',
#             'Authorization': 'Basic UElUQjo4NTMwNWFlMjg1ZjVhNzk1OWY4OWE4YWY5Y2FhNWY1Nw=='
#         }
#
#         response_gprs_api = []
#         response_message = ""
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 response_gprs_api = response.json()  # Get the response data from the external API
#                 response_message = "Data fetched successfully"
#             else:
#                 response_message = "Data Not Fetch"
#         except:
#             response_message = "Url Error"
#
#         ### API RESPONSE CHECK ###
#         total_len = len(response_gprs_api)
#         if len(response_gprs_api) > 0:  ### RECORD EXIST ###
#             total_vendor_record = len(response_gprs_api['Table'])
#
#             vehicle_gprs_response_api = response_gprs_api['Table']
#             vehicle_gprs_response_api_len = len(vehicle_gprs_response_api)
#             for g in range(vehicle_gprs_response_api_len):
#                 ck_vehicle_code = vehicle_gprs_response_api[g]['VehicleID']
#                 ck_vendor_date_time = vehicle_gprs_response_api[g]['GpsTime']
#                 ### TRACKER RAW DATA (START)
#
#                 try:
#                     if '.' in ck_vendor_date_time:
#                         ck_vendor_date_time = ck_vendor_date_time.split('.')[0]  # Remove the decimal part
#
#                     _ck_vendor_date_time = datetime.datetime.fromisoformat(ck_vendor_date_time)
#                     formatted_vendor_date_time = _ck_vendor_date_time.strftime(
#                         format_str_date_time)  # Format as a string
#                     # print("Valid ISO format:")
#                 except ValueError:
#                     # Parse into datetime object
#                     formatted_vendor_date_time = datetime.strptime(ck_vendor_date_time, format_str_date_time)
#
#                 GetTrackerRawData = TrackerRawData.objects.filter(vehicle_code_id=vehicle_code,
#                                                                   vendor_date_time=formatted_vendor_date_time)
#                 if len(GetTrackerRawData) == 0:
#                     auto_gprs_code = AutoGenerateCodeForModel(TrackerRawData, "gprs_raw_code", "GPRS-")
#
#                     vt_latitude = vehicle_gprs_response_api[g]['Lat']
#                     vt_longitude = vehicle_gprs_response_api[g]['Long']
#                     get_feature_coordinate = "POINT(" + str(vt_longitude) + " " + str(vt_latitude) + ")"
#
#                     InstTrackerRawData = TrackerRawData(
#                         gprs_raw_code=auto_gprs_code,
#                         vehicle_code_id=vehicle_code,
#                         terminal_no=vehicle_gprs_response_api[g]['TerminalNo'],
#                         geom=get_feature_coordinate,
#                         latitude=vt_latitude,
#                         longitude=vt_longitude,
#                         g_status=vehicle_gprs_response_api[g]['Veh_Status'],
#                         vehicle_status=vehicle_gprs_response_api[g]['Veh_Status'],
#                         device_status=vehicle_gprs_response_api[g]['Dev_status'],
#                         vendor_date_time=formatted_vendor_date_time,
#                         system_date_time=vehicle_gprs_response_api[g]['RecTime'],
#                         speed=vehicle_gprs_response_api[g]['Speed'],
#                         distance=vehicle_gprs_response_api[g]['Distance'],
#                         direction=vehicle_gprs_response_api[g]['Direction'],
#                         mileage=vehicle_gprs_response_api[g]['Mileage_Val'],
#                         push_status="Pending",
#                         created_at=current_data_time,
#                         created_by="admin"
#                     )
#                     InstTrackerRawData.save()
#                     # TRACKER RAW DATA (END)
#                 # RECORD FOUND (END)
#             ### LOOP END
#
#             tracker_gprs_length = TrackerRawData.objects.filter(
#                 vehicle_code_id=vehicle_code,
#                 vendor_date_time__date=selected_date
#             ).aggregate(
#                 total_count=Count('id')
#             )['total_count']
#
#             ### UPDATE VEHICLE SCHEDULE GPRS API RECORD
#             UpdateVehiclScheduleGPRSApi = VehicleScheduleGPRSApi.objects.get(
#                 veh_sch_date=selected_date,
#                 vehicle_code_id=vehicle_code
#             )
#             UpdateVehiclScheduleGPRSApi.retrieve_record = tracker_gprs_length
#
#             # current_data_time
#             ### DATE CONVERT INTO STRING FORMAT
#             str_current_data_time = current_data.strftime(format_str_date)
#             if str_current_data_time != selected_date:
#                 if total_vendor_record >= tracker_gprs_length:
#                     UpdateVehiclScheduleGPRSApi.process_status = "Completed"
#
#             UpdateVehiclScheduleGPRSApi.save()
#             ### UPDATE VEHICLE SCHEDULE GPRS API RECORD
#
#         ### API RESPONSE LOOP ###
#
#     ### RECORD EXIST ###
#
#     ### CHECK VEHICLE GPRS LIST (END)
#


# @shared_task
# # UTSPostVTMSBulkBackend_2Min
# def UTSPostVTMSBulkBackend_DayWise(vehicle_code, str_selected_date):
#     """
#     Function to fetch and post multiple vehicle tracker data points to external VTMS API
#     """
#     data_to_send = []  # List to hold data to be sent in bulk
#
#     try:
#
#         try:
#             vehicle = VehicleData.objects.get(vehicle_code=vehicle_code)
#             get_pitb_vehicle_code = vehicle.pitb_code
#         except VehicleData.DoesNotExist:
#             return {
#                 "error": f"Vehicle with code {vehicle_code} not found",
#                 "status": 404
#             }
#
#         dt_selected_date = datetime.datetime.strptime(str_selected_date, "%Y-%m-%d")
#         # Get tracker data records for this vehicle on the selected date (limited to 10)
#         datas = TrackerRawData.objects.filter(vehicle_code_id=vehicle,
#                                               vendor_date_time__date=dt_selected_date,
#                                               push_status="Pending").order_by('id')
#
#         if not datas:
#             return {
#                 "error": "No tracker data found for this vehicle on the selected date",
#                 "status": 404
#             }
#
#         # Process each data record in the loop
#         for data in datas:
#             # Extract 'Off' and 'On' as whole words
#             status_match = re.findall(r'\b(Off|On)\b', data.device_status)
#             set_engine_status = status_match[0] if status_match else "Off"
#
#             # Make sure vehicle_status matches API requirements [moving/idle/waiting/still]
#             set_vehicle_status = "moving"
#             if data.device_status == "ACC Off,Parked":
#                 set_vehicle_status = "waiting"
#             elif data.device_status == "ACC On,Idle":
#                 set_vehicle_status = "idle"
#
#             # Define the datetime format string
#             format_str = '%Y-%m-%d %H:%M:%S'
#
#             datetime_from_5_hour_str = (data.vendor_date_time + datetime.timedelta(hours=5)).strftime(format_str)
#             dj_timestamp = datetime.datetime.strptime(datetime_from_5_hour_str, format_str)
#
#             ### DATE CONVERT INTO STRING FORMAT
#             work_date_str = dj_timestamp.strftime(format_str)
#             timestamp = data.vendor_date_time.strftime(work_date_str)
#
#             # Generate a 25-character UUID without hyphens
#             short_uuid = uuid.uuid4().hex[:25]
#
#             # Format data for the external API - ensuring proper format for all fields
#             extracted_data = {
#                 "vehicle_no": str(get_pitb_vehicle_code),
#                 "uuid": short_uuid,  # Explicitly using 25-char hex UUID
#                 "lat": float(data.latitude),
#                 "long": float(data.longitude),
#                 "speed": float(data.speed),
#                 "distance": float(data.distance),
#                 "working_hour": 0,
#                 "timestamp": timestamp,
#                 "vehicle_status": set_vehicle_status,  # Must be one of: moving/idle/waiting/still
#                 "engine_status": set_engine_status.lower()  # Must be: on/off
#             }
#             data_to_send.append(extracted_data)
#
#         if len(data_to_send) > 0:
#             headers = {
#                 "authkey": "SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1",
#                 "Content-Type": "application/json",
#                 "Accept": "application/json"
#             }
#
#             api_url = "https://elgcd-ms.punjab.gov.pk/api/vtms/post-vtms-bulk-data"
#
#             # Try with explicit form data
#             response = requests.post(
#                 url=api_url,
#                 json=data_to_send,
#                 headers=headers,
#                 timeout=30
#             )
#
#             # Log the response for debugging
#             print(f"Response status: {response.status_code}")
#             print(f"Response body: {response.text}")
#
#             ### UPDATED TRACKER RAW DATA LATEST ROW
#             TrackerRawData.objects.filter(vehicle_code_id=vehicle,
#                                           vendor_date_time__date=dt_selected_date,
#                                           push_status="Pending").update(push_status='Completed')
#
#             return {
#                 "api_response": {
#                     "status_code": response.status_code,
#                     "body": response.json() if response.status_code in [200, 201] else response.text
#                 },
#                 "data_sent": data_to_send,
#                 "count": len(data_to_send),
#                 "status": 200 if response.status_code in [200, 201] else response.status_code
#             }
#
#     except Exception as e:
#         return {
#             "error": str(e),
#             "status": 500
#         }

# @shared_task
# UTSPostVTMSPostData_local_database_single_vehicle
# def UTSPostVTMSBulkBackgroundTask_DayWise():
#     step_competed = 0
#     try:
#         logger.info("Starting Step 1: Generating working schedule")
#         current_date = datetime.datetime.now().date()
#         step1 = GenerateWorkingWithVehicleSchedule_Function(current_date)
#         step_competed += 1
#         logger.info(f"Step 1 completed")
#         logger.info("Starting Step 2: Fetching vehicle data from vendor")
#         step2 = UTSPostVTMSPostData_local_database_single_vehicle('279376', '2025-05-06')
#         step_competed += 1
#         logger.info(f"Step 2 completed")
#         step3 = UTSPostVTMSBulkBackend_DayWise()
#         step_competed += 1
#         logger.info(f"Step 3 completed")
#
#     except Exception as e:
#         logger.error(f"Error in UTSPostVTMSBulkBackgroundTask: {e}")
#         return {
#             "error": str(e),
#             "status": 500,
#             "step_completed": step_competed
#         }
#
#     return step_competed


# 7/4/2025
# New task for pending vehicles


def ResponseTrackerGPRSRawApi_By_Vendor_Function(vehicle_code, from_date, to_date):
    ### Base URL
    base_url = "https://labs3.unitedtracker.com/api/Trackers/GetVehicleHistoryByUserName"

    ### Define parameters ###
    params = {
        "UserName": "AKHTAR6792",
        "Password": "AKHTAR@6792",
        "VehicleID": vehicle_code,
        "fromDate": from_date,  # 2025-04-15 14:00:02
        "toDate": to_date  # toDate=2025-04-15 14:10:02
    }

    ### Generate URL with dynamic dates
    url = f"{base_url}?{urlencode(params)}"
    headers = {
        'API_KEY': '7b6f169d544e4eda4b2b263e6bffe50d',
        'Authorization': 'Basic UElUQjo4NTMwNWFlMjg1ZjVhNzk1OWY4OWE4YWY5Y2FhNWY1Nw=='
    }

    response_data = []
    response_message = ""
    try:
        logger.info(f"Requesting tracking data: VehicleID={vehicle_code}, from={from_date}, to={to_date}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()  # Get the response data from the external API
            response_message = "Data fetched successfully"

            # Safely log the first record if it exists
            if isinstance(response_data, dict) and 'Table' in response_data and response_data['Table']:
                logger.info(f"First record: {json.dumps(response_data['Table'][0], indent=2)}")
            else:
                logger.warning(
                    f"Response received but no records found in Table. Response: {str(response_data)[:200]}...")
        else:
            response_message = f"Data Not Fetch - Status code: {response.status_code}"
            logger.error(f"API request failed with status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        response_message = f"Error: {str(e)}"
        logger.error(f"Exception when calling API: {str(e)}")
        # Return empty dict with Table key to prevent further errors
        response_data = {"Table": []}

    # Ensure response_data has a 'Table' key, even if empty
    if not isinstance(response_data, dict):
        response_data = {"Table": []}
    elif 'Table' not in response_data:
        response_data['Table'] = []

    return response_data


@shared_task
def process_pending_vehicle_gprs_data():
    """
    Celery task to process all vehicles with 'Pending' status in VehicleScheduleGPRSApi.
    Fetches GPRS data for them and updates their status.
    """
    format_str_date = "%Y-%m-%d"
    format_str_date_time = "%Y-%m-%d %H:%M:%S"
    current_data_time = datetime.now()

    # Find all pending vehicle schedule records
    pending_schedules = VehicleScheduleGPRSApi.objects.filter(process_status="Pending")

    logger.info(f"Found {pending_schedules.count()} pending vehicle schedules to process")

    results = []

    for schedule in pending_schedules:
        vehicle_id = schedule.vehicle_code_id
        selected_date = schedule.veh_sch_date

        logger.info(f"Processing vehicle {vehicle_id} for date {selected_date}")

        # Generate schedule first (same as original function)
        GenerateWorkingWithVehicleSchedule_Function(selected_date)

        # Set time range for the full day
        start_of_day_time_str = '00:00:00'
        end_of_day_time_str = '23:59:59'

        # Combine date and time into string
        datetime_from = selected_date.strftime(format_str_date) + " " + start_of_day_time_str
        datetime_to = selected_date.strftime(format_str_date) + " " + end_of_day_time_str

        # Get vendor server response from tracker GPRS raw data API function
        response_gprs_api = ResponseTrackerGPRSRawApi_By_Vendor_Function(vehicle_id, datetime_from, datetime_to)

        # Process API response
        if len(response_gprs_api) > 0:  # Record exists
            total_vendor_record = len(response_gprs_api['Table'])

            vehicle_gprs_response_api = response_gprs_api['Table']
            vehicle_gprs_response_api_len = len(vehicle_gprs_response_api)

            for g in range(vehicle_gprs_response_api_len):
                ck_vehicle_code = vehicle_gprs_response_api[g]['VehicleID']
                ck_vendor_date_time = str(vehicle_gprs_response_api[g]['GpsTime'])
                ck_api_latitude = vehicle_gprs_response_api[g]['Lat']
                ck_api_longitude = vehicle_gprs_response_api[g]['Long']

                try:
                    if '.' in ck_vendor_date_time:
                        ck_vendor_date_time = ck_vendor_date_time.split('.')[0]  # Remove the decimal part

                    _ck_vendor_date_time = datetime.fromisoformat(ck_vendor_date_time)
                    formatted_vendor_date_time = _ck_vendor_date_time.strftime(format_str_date_time)
                except ValueError:
                    # Parse into datetime object
                    formatted_vendor_date_time = datetime.strptime(ck_vendor_date_time, format_str_date_time)

                # Check if tracker raw data exists
                GetTrackerRawData = TrackerRawData.objects.filter(
                    vehicle_code_id=ck_vehicle_code,
                    vendor_date_time=ck_vendor_date_time,
                    latitude=ck_api_latitude,
                    longitude=ck_api_longitude
                )

                if len(GetTrackerRawData) == 0:
                    # Create new tracker raw data entry
                    gprs_code_number = int(TrackerRawData.objects.order_by('-id').values_list('id', flat=True).first())
                    auto_gprs_code = f"GPRS-{gprs_code_number}"

                    # Set point geom
                    get_feature_coordinate = f"POINT({ck_api_longitude} {ck_api_latitude})"

                    # Create new row in tracker raw data
                    TrackerRawData.objects.create(
                        gprs_raw_code=auto_gprs_code,
                        vehicle_code_id=ck_vehicle_code,
                        terminal_no=vehicle_gprs_response_api[g]['TerminalNo'],
                        geom=get_feature_coordinate,
                        latitude=ck_api_latitude,
                        longitude=ck_api_longitude,
                        g_status=vehicle_gprs_response_api[g]['Veh_Status'],
                        vehicle_status=vehicle_gprs_response_api[g]['Veh_Status'],
                        device_status=vehicle_gprs_response_api[g]['Dev_status'],
                        vendor_date_time=vehicle_gprs_response_api[g]['GpsTime'],
                        system_date_time=vehicle_gprs_response_api[g]['RecTime'],
                        speed=vehicle_gprs_response_api[g]['Speed'],
                        distance=vehicle_gprs_response_api[g]['Distance'],
                        direction=vehicle_gprs_response_api[g]['Direction'],
                        mileage=vehicle_gprs_response_api[g]['Mileage_Val'],
                        created_at=current_data_time,
                        created_by="admin"
                    )

            # Count tracker GPRS records for this vehicle on this date
            tracker_gprs_length = TrackerRawData.objects.filter(
                vehicle_code_id=ck_vehicle_code,
                vendor_date_time__date=selected_date
            ).aggregate(
                total_count=Count('id')
            )['total_count']

            # Update vehicle schedule GPRS API record
            schedule.retrieve_record = tracker_gprs_length

            # Mark as completed if all records retrieved
            if tracker_gprs_length >= total_vendor_record:
                schedule.process_status = "Completed"

            schedule.save()

            # Calculate and prepare results (line geometry, distance, etc.)
            django_datetime_from = parse_datetime(datetime_from)
            django_datetime_to = parse_datetime(datetime_to)

            # Get tracker data points
            tracker_raw_gprs_lists = list(TrackerRawData.objects.filter(
                vehicle_code_id=vehicle_id,
                vendor_date_time__gte=django_datetime_from,
                vendor_date_time__lte=django_datetime_to
            ).annotate(
                x=RawSQL("ST_X(geom)", []),
                y=RawSQL("ST_Y(geom)", [])
            ).values(
                "x", "y", "vehicle_code_id", "g_status", "system_date_time",
                "vendor_date_time", "device_status", "max_speed", "speed",
                "vehicle_status", "direction", "distance", "mileage"
            ).order_by('id'))

            # Calculate track length
            vehicle_tracks = TrackerRawData.objects.filter(
                vehicle_code_id=vehicle_id,
                vendor_date_time__gte=django_datetime_from,
                vendor_date_time__lte=django_datetime_to
            ).values('vehicle_code_id').annotate(
                line=MakeLine('geom'),  # Create a line from grouped points
                length=Length(MakeLine('geom'))  # Calculate line length
            )

            # Convert to GeoJSON for results
            vehicle_tracks_length = [
                {
                    "vehicle_code_id": track["vehicle_code_id"],
                    "length_meters": track["length"].m,  # Convert to meters
                    "line_geojson": track["line"].geojson  # Convert to GeoJSON
                }
                for track in vehicle_tracks
            ]

            # Add to results
            result = {
                'vehicle_id': vehicle_id,
                'date': selected_date.strftime(format_str_date),
                'points_count': len(tracker_raw_gprs_lists),
                'message': "Success",
                'tracker_raw_gprs_lists': tracker_raw_gprs_lists,
                'vehicle_tracks_length': vehicle_tracks_length,
            }

            results.append(result)

        else:
            logger.warning(f"No GPRS data found for vehicle {vehicle_id} on {selected_date}")

    # Log summary
    logger.info(f"Processed {len(results)} vehicles with pending status")

    return results
