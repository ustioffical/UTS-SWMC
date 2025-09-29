import json
import datetime
import requests

from django.http import HttpResponse
from django.shortcuts import render

from AppAdmin.utils import *
from AppVehicle.views import *
from VTMS.views import *


# Create your views here.
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def FetchUnionCouncilFeatureView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from (SELECT geom, uc_code, uc_name FROM tbl_union_council_boundary ) as foo) As f )  As fc; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchLanduseBoundaryFeatureView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from (SELECT geom, landuse_code, landuse_name FROM tbl_landuse_boundary ) as foo) As f )  As fc; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchAdministrativeBoundaryFeatureView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from (SELECT geom, admin_code, admin_name, admin_type FROM tbl_administrative_boundary ) as foo) As f )  As fc; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def PITBApi_TransmissionDataListView(request):
    message = ""
    # cursor = connections['default'].cursor()
    template_name = "PITBApi_TransmissionDataList.html"

    vehicle_data_list = VehicleData.objects.all().order_by('vehicle_type')

    # ### RETRIEVE DATE FROM VENDOR APP AND PUSH DATA TO PITB APP (POST VTMS DATA SINGLE)
    # APIpostVTMSPostData_local_database_single_vehicle('279376', '2025-05-06')

    page_title = "Create Network"
    params = {
        'vehicle_data_list': vehicle_data_list,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


def PushDataPITBServer_PostVTMSDataView(request):
    get_vehicle_id = request.POST['vehicle_code']
    get_start_date = request.POST['selected_date']

    ### RETRIEVE DATE FROM VENDOR APP AND PUSH DATA TO PITB APP (POST VTMS DATA SINGLE)
    # APIpostVTMSPostData_local_database_single_vehicle(get_vehicle_id, get_start_date)
    APIpostVTMSPostData_local_database_single_vehicle('278905', '2025-05-06')

    message = "Success"
    params = {
        'message': message,
    }

    return HttpResponse(json.dumps(params, default=date_handler))

    # Convert string dates to datetime objects


### RETRIEVE DATE FROM VENDOR APP AND PUSH DATA TO PITB APP (POST VTMS DATA SINGLE)
def APIpostVTMSPostData_local_database_single_vehicle(vehicle_code: str, selected_date: str):
    format_str_date = "%Y-%m-%d"
    format_str_date_time = "%Y-%m-%d %H:%M:%S"
    current_data_time = datetime.datetime.now()
    current_data = current_data_time.date()

    ### STEP-1 GENERATE WORKING SCHEDULA WITH VEHICLE SCHEDULE IN SYSTEM FUNCTION
    Gen_Schedule = GenerateWorkingWithVehicleSchedule_Function(selected_date)

    ### CHECK VEHICLE VENDOR RECORD EQUAL TO DUMP RECORD WITH STATUS
    fetch_vehicle_sche_record = VehicleScheduleGPRSApi.objects.get(veh_sch_date=selected_date,
                                                                   vehicle_code_id=vehicle_code)
    ck_process_status = fetch_vehicle_sche_record.process_status

    if ck_process_status == "Pending":  ### PROCESS STATUS "PENDING" ###
        ### CHECK VEHICLE GPRS LIST (START)

        start_of_day_time_str = '00:00:00'
        end_of_day_time_str = '23:59:59'
        ### DATE CONVERT INTO STRING FORMAT
        work_date_str = selected_date

        ### COMBINE DATE AND TIME INTO STRING
        datetime_from = work_date_str + " " + start_of_day_time_str  ## "2025-02-27 00:00:00"
        datetime_to = work_date_str + " " + end_of_day_time_str  ## "2025-02-27 23:59:59"

        ### GET VENDOR SERVER RESPONSE FROM TRACKER GPRS RAW DATA API FUNCTION
        response_gprs_api = ResponseTrackerGPRSRawApi_By_Vendor_Function(vehicle_code, datetime_from, datetime_to)

        ### API RESPONSE CHECK ###
        total_len = len(response_gprs_api)
        if len(response_gprs_api) > 0:  ### RECORD EXIST ###
            total_vendor_record = len(response_gprs_api['Table'])

            vehicle_gprs_response_api = response_gprs_api['Table']
            vehicle_gprs_response_api_len = len(vehicle_gprs_response_api)
            for g in range(vehicle_gprs_response_api_len):
                ck_vehicle_code = vehicle_gprs_response_api[g]['VehicleID']
                ck_vendor_date_time = vehicle_gprs_response_api[g]['GpsTime']
                ### TRACKER RAW DATA (START)

                try:
                    if '.' in ck_vendor_date_time:
                        ck_vendor_date_time = ck_vendor_date_time.split('.')[0]  # Remove the decimal part

                    _ck_vendor_date_time = datetime.datetime.fromisoformat(ck_vendor_date_time)
                    formatted_vendor_date_time = _ck_vendor_date_time.strftime(
                        format_str_date_time)  # Format as a string
                    # print("Valid ISO format:")
                except ValueError:
                    # Parse into datetime object
                    formatted_vendor_date_time = datetime.strptime(ck_vendor_date_time, format_str_date_time)

                GetTrackerRawData = TrackerRawData.objects.filter(vehicle_code_id=vehicle_code,
                                                                  vendor_date_time=formatted_vendor_date_time)
                if len(GetTrackerRawData) == 0:
                    auto_gprs_code = AutoGenerateCodeForModel(TrackerRawData, "gprs_raw_code", "GPRS-")

                    vt_latitude = vehicle_gprs_response_api[g]['Lat']
                    vt_longitude = vehicle_gprs_response_api[g]['Long']
                    get_feature_coordinate = "POINT(" + str(vt_longitude) + " " + str(vt_latitude) + ")"

                    InstTrackerRawData = TrackerRawData(
                        gprs_raw_code=auto_gprs_code,
                        vehicle_code_id=vehicle_code,
                        terminal_no=vehicle_gprs_response_api[g]['TerminalNo'],
                        geom=get_feature_coordinate,
                        latitude=vt_latitude,
                        longitude=vt_longitude,
                        g_status=vehicle_gprs_response_api[g]['Veh_Status'],
                        vehicle_status=vehicle_gprs_response_api[g]['Veh_Status'],
                        device_status=vehicle_gprs_response_api[g]['Dev_status'],
                        vendor_date_time=formatted_vendor_date_time,
                        system_date_time=vehicle_gprs_response_api[g]['RecTime'],
                        speed=vehicle_gprs_response_api[g]['Speed'],
                        distance=vehicle_gprs_response_api[g]['Distance'],
                        direction=vehicle_gprs_response_api[g]['Direction'],
                        mileage=vehicle_gprs_response_api[g]['Mileage_Val'],
                        push_status="Pending",
                        created_at=current_data_time,
                        created_by="admin"
                    )
                    InstTrackerRawData.save()
                    # TRACKER RAW DATA (END)
                # RECORD FOUND (END)
            ### LOOP END

            tracker_gprs_length = TrackerRawData.objects.filter(
                vehicle_code_id=vehicle_code,
                vendor_date_time__date=selected_date
            ).aggregate(
                total_count=Count('id')
            )['total_count']

            ### UPDATE VEHICLE SCHEDULE GPRS API RECORD
            UpdateVehiclScheduleGPRSApi = VehicleScheduleGPRSApi.objects.get(
                veh_sch_date=selected_date,
                vehicle_code_id=vehicle_code
            )
            UpdateVehiclScheduleGPRSApi.retrieve_record = tracker_gprs_length

            # current_data_time
            ### DATE CONVERT INTO STRING FORMAT
            str_current_data_time = current_data.strftime(format_str_date)
            if str_current_data_time != selected_date:
                if total_vendor_record >= tracker_gprs_length:
                    UpdateVehiclScheduleGPRSApi.process_status = "Completed"

            UpdateVehiclScheduleGPRSApi.save()
            ### UPDATE VEHICLE SCHEDULE GPRS API RECORD

        ### API RESPONSE LOOP ###

    ### RECORD EXIST ###

    ### CHECK VEHICLE GPRS LIST (END)

    # UTSPostVTMS(vehicle_code, selected_date)
    UTSPostVTMSBulk(vehicle_code, selected_date)
