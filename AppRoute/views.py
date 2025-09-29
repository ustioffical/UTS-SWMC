import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from AppAdmin.utils import *
from AppRoute.models import *
from AppSetting.models import TownBoundary
from AppVehicle.views import *

# Create your views here.
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def CreateNetworkWithListView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "CreateNetwork.html"

    town_boundary = TownBoundary.objects.all().order_by('town_name')

    page_title = "Create Network"
    params = {
        # 'container_list': container_list,
        'town_boundary': town_boundary,
        # 'feature_lists': feature_lists,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


# AJAX VIEW
def FetchOSMRoadNetworkByFilterView(request):
    message = ""
    cursor = connections['default'].cursor()

    get_town_code = request.POST['town_code']
    get_zone_code = request.POST['zone_code']
    get_mc_code = request.POST['mc_code']

    se_filter_query = ""
    if get_town_code == "NA":
        pass
    if get_zone_code == "NA":
        pass
    if get_zone_code == "NA":
        pass

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from ( WITH clip AS( WITH search AS( SELECT geom FROM tbl_town_boundary ) SELECT st_intersection(ST_MakeValid(osm.geom), ST_MakeValid(search.geom)) as clip_geom, fclass, name, oneway, maxspeed, layer, bridge, tunnel FROM search, tbl_osm_network_download AS osm WHERE  st_intersects(search.geom, osm.geom) ) SELECT ST_GeomFromText(ST_AsTEXT((ST_DUMP(clip_geom)).geom), 4326) AS geom, fclass, name, oneway, maxspeed, layer, bridge, tunnel FROM clip ) as foo) As f )  As fc ";
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def DesignRouteNetworkView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "DesignRoute.html"

    # container_list = ContainerData.objects.all().order_by('mc_code',
    #                                                       'container_name')
    #
    query_container_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, container_code, container_name, status FROM tbl_container_data WHERE status = 'Active'; ";
    cursor.execute(query_container_feature)
    container_feature = DictinctFetchAll(cursor)
    #
    town_boundary = TownBoundary.objects.all().order_by('town_name')

    page_title = "Create Network"
    params = {
        'container_feature': container_feature,
        'town_boundary': town_boundary,
        # 'feature_lists': feature_lists,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


# AJAX VIEW
def FetchRouteNetworkScheduleFeatureView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from ( WITH route AS (SELECT route_code_id, sche_group_code, sche_group_name AS name, geom FROM tbl_route_network_schedule AS rns INNER JOIN tbl_route_network_boundary rnb ON rns.route_code_id = rnb.route_code WHERE rns.status = 'Active') SELECT route_code_id, sche_group_code, name, geom FROM route ) as foo) As f )  As fc; ";
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


# def VehicleRouteReportView(request):
#     template = "Vehicle/VehicleRouteReport11.html"
#     # Get all distinct vehicle types (to always populate the dropdown)
#     vehicle_types = VehicleType.objects.values_list('vehicle_type_name', flat=True).distinct()
#
#     # Get search query and selected vehicle type from GET parameters
#     search_query = request.GET.get('search_vehicle', '')
#     selected_type = request.GET.get('cmd_vehicle_type', 'NA')
#     # Get start and end datetime from GET parameters
#     from_datetime = request.GET.get('from_datetime', '')
#     to_datetime = request.GET.get('to_datetime', '')
#     selected_vehicle_id = request.GET.get('cmd_vehicle_list', 'NA')
#
#     vehicle_ids = []
#     tracker_raw_gprs_lists = []
#     vehicle_tracks_length = []
#     message = ""
#     # If a vehicle type is explicitly selected (not "NA"), filter by type.
#     if selected_type and selected_type != "NA":
#         vehicles = VehicleData.objects.filter(vehicle_type=selected_type)
#         if search_query:
#             vehicles = vehicles.filter(vehicle_code__icontains=search_query)
#         vehicle_ids = vehicles.values_list('vehicle_code', flat=True).distinct()
#     # If no type is selected but a search query is provided, filter on vehicle code
#     elif search_query:
#         vehicle_ids = VehicleData.objects.filter(vehicle_code=search_query) \
#             .values_list('vehicle_code', flat=True) \
#             .distinct()
#
#     # Check if all required parameters are provided to retrieve trip history
#     if from_datetime and to_datetime and selected_vehicle_id != 'NA':
#         # Call the function and extract the JSON data from the response
#         print("Execution the fucntion")
#         logger.info("Sir function is now being executed.")
#         response = FetchSingleVehicleTripHistoryData(selected_vehicle_id, from_datetime, to_datetime)
#         if response:
#             # Parse the JSON content
#             data = json.loads(response.content.decode('utf-8'))
#             tracker_raw_gprs_lists = data.get('tracker_raw_gprs_lists', [])
#             vehicle_tracks_length = data.get('vehicle_tracks_length', [])
#             message = data.get('message', "")
#
#     context = {
#         'vehicle_types': vehicle_types,
#         'vehicle_ids': vehicle_ids,
#         'search_query': search_query,
#         'selected_type': selected_type,
#         'from_datetime': from_datetime,
#         'to_datetime': to_datetime,
#         'selected_vehicle_id': selected_vehicle_id,
#         'tracker_raw_gprs_lists': tracker_raw_gprs_lists,
#         'vehicle_tracks_length': vehicle_tracks_length,
#         'message': message
#     }
#     return render(request, template, context)


# This is the function which was converted from view to function
# def FetchSingleVehicleTripHistoryData(get_vehicle_id, get_start_date, get_end_date):
#     logger.info("FetchSingleVehicleTripHistoryData is now being executed.")
#
#     format_str_date = "%Y-%m-%d"
#     format_str_date_time = "%Y-%m-%d %H:%M:%S"
#     current_data_time = datetime.datetime.now()
#
#     ### IF DATE NOT EXIST
#     if isinstance(get_start_date, datetime.datetime):
#         dt_start_date = get_start_date.date()
#     else:
#         try:
#             # Check if it's in HTML5 format
#             if 'T' in get_start_date:
#                 if len(get_start_date.split(':')) == 2:  # Missing seconds
#                     get_start_date = get_start_date + ":00"  # Add seconds
#                 get_start_date = get_start_date.replace('T', ' ')  # Replace T with space
#             dt_start_date = datetime.datetime.strptime(get_start_date, format_str_date_time).date()
#         except ValueError:
#             # If that fails, try to parse just the date part
#             dt_start_date = datetime.datetime.strptime(get_start_date.split('T')[0], format_str_date).date()
#
#     if isinstance(get_end_date, datetime.datetime):
#         dt_end_date = get_end_date.date()
#     else:
#         try:
#             # Check if it's in HTML5 format
#             if 'T' in get_end_date:
#                 if len(get_end_date.split(':')) == 2:  # Missing seconds
#                     get_end_date = get_end_date + ":00"  # Add seconds
#                 get_end_date = get_end_date.replace('T', ' ')  # Replace T with space
#             dt_end_date = datetime.datetime.strptime(get_end_date, format_str_date_time).date()
#         except ValueError:
#             # If that fails, try to parse just the date part
#             dt_end_date = datetime.datetime.strptime(get_end_date.split('T')[0], format_str_date).date()
#     ### FETCH NO OF DATE WHICH IS NOT EXIST
#     range_date_list = []
#     between_date_list = []
#     current = dt_start_date
#     while current <= dt_end_date:
#         ### IF VEHICLE SCHEDULE DATE EXIST OR NOT
#         vehicle_schedule_record = VehicleScheduleGPRSApi.objects.filter(veh_sch_date=current,
#                                                                         vehicle_code_id=get_vehicle_id)
#         if len(vehicle_schedule_record) == 0:  ## IF SELECTED DATE EXIST
#             between_date_list.append(current)
#
#         range_date_list.append(current)
#         current += datetime.timedelta(days=1)
#     # print(date_list)
#     # string_dates = [d.strftime("%Y-%m-%d") for d in date_list]
#
#     if len(between_date_list) > 0:
#         for i in range(len(between_date_list)):
#             converted_date_inst = between_date_list[i]
#
#             ### IF CURRENT DATE EXIST OR NOT
#             current_date_records = WorkScheduleGPRSApi.objects.filter(work_date=converted_date_inst)
#             if len(current_date_records) == 0:  ## IF CURRENT DATE EXIST
#                 auto_gprs_code = AutoGenerateCodeForModel(WorkScheduleGPRSApi, "code", "WS-")
#                 ### GPRS - WORKING SCHEDULE API (START)
#                 InstWorkSche = WorkScheduleGPRSApi(
#                     code=auto_gprs_code,
#                     work_date=converted_date_inst,
#                     run_count=0,
#                     process_status="Pending",
#                     description="Sync-Current",
#                     created_at=current_data_time,
#                     created_by="admin"
#                 )
#                 InstWorkSche.save()
#                 ### GPRS - WORKING SCHEDULE API (END)
#
#             ### GENERATE VEHICLE SCHEDULA IN SYSTEM FUNCTION
#             GenerateVehicleSchedule_Function("", converted_date_inst)
#         ### LOOP (END)
#     ### CHECK SCHEDULE ADDED OR NOT (END)
#
#     ### CHECK VEHICLE VENDOR RECORD EQUAL TO DUMP RECORD WITH STATUS
#     fetch_vehicle_sche_record = VehicleScheduleGPRSApi.objects.get(veh_sch_date=dt_start_date,
#                                                                    vehicle_code_id=get_vehicle_id)
#     ck_process_status = fetch_vehicle_sche_record.process_status
#
#     if ck_process_status == "Pending":  ### PROCESS STATUS "PENDING" ###
#         ### CHECK VEHICLE GPRS LIST (START)
#
#         start_of_day_time_str = '00:00:00'
#         end_of_day_time_str = '23:59:59'
#         ### DATE CONVERT INTO STRING FORMAT
#         work_date_str = dt_start_date.strftime(format_str_date)
#
#         ### COMBINE DATE AND TIME INTO STRING
#         datetime_from = work_date_str + " " + start_of_day_time_str  ## "2025-02-27 00:00:00"
#         datetime_to = work_date_str + " " + end_of_day_time_str  ## "2025-02-27 23:59:59"
#
#         ### GET VENDOR SERVER RESPONSE FROM TRACKER GPRS RAW DATA API FUNCTION
#         response_gprs_api = ResponseTrackerGPRSRawApi_By_Vendor_Function(get_vehicle_id, datetime_from, datetime_to)
#         logger.info("Vendor Response JSON: %s", json.dumps(response_gprs_api))
#         ### API RESPONSE CHECK ###
#         if len(response_gprs_api) > 0:  ### RECORD EXIST ###
#             total_vendor_record = len(response_gprs_api['Table'])
#
#             vehicle_gprs_response_api = response_gprs_api['Table']
#             vehicle_gprs_response_api_len = len(vehicle_gprs_response_api)
#             for g in range(vehicle_gprs_response_api_len):
#                 ck_vehicle_code = vehicle_gprs_response_api[g]['VehicleID']
#                 tr_vendor_date_time = vehicle_gprs_response_api[g]['GpsTime']
#                 tr_system_date_time = vehicle_gprs_response_api[g]['RecTime']
#                 ### TRACKER RAW DATA (START)
#
#                 GetTrackerRawData = TrackerRawData.objects.filter(vehicle_code_id=ck_vehicle_code,
#                                                                   system_date_time=tr_system_date_time,
#                                                                   vendor_date_time=tr_vendor_date_time)
#                 if len(GetTrackerRawData) == 0:
#                     auto_gprs_code = AutoGenerateCodeForModel(TrackerRawData, "gprs_raw_code", "GPRS-")
#
#                     vt_latitude = vehicle_gprs_response_api[g]['Lat']
#                     vt_longitude = vehicle_gprs_response_api[g]['Long']
#                     get_feature_coordinate = "POINT(" + str(vt_longitude) + " " + str(vt_latitude) + ")"
#
#                     InstTrackerRawData = TrackerRawData(
#                         gprs_raw_code=auto_gprs_code,
#                         vehicle_code_id=ck_vehicle_code,
#                         terminal_no=vehicle_gprs_response_api[g]['TerminalNo'],
#                         geom=get_feature_coordinate,
#                         latitude=vt_latitude,
#                         longitude=vt_longitude,
#                         g_status=vehicle_gprs_response_api[g]['Veh_Status'],
#                         vehicle_status=vehicle_gprs_response_api[g]['Veh_Status'],
#                         device_status=vehicle_gprs_response_api[g]['Dev_status'],
#                         vendor_date_time=vehicle_gprs_response_api[g]['GpsTime'],
#                         system_date_time=vehicle_gprs_response_api[g]['RecTime'],
#                         speed=vehicle_gprs_response_api[g]['Speed'],
#                         distance=vehicle_gprs_response_api[g]['Distance'],
#                         direction=vehicle_gprs_response_api[g]['Direction'],
#                         mileage=vehicle_gprs_response_api[g]['Mileage_Val'],
#                         created_at=current_data_time,
#                         created_by="admin"
#                     )
#                     InstTrackerRawData.save()
#                     # TRACKER RAW DATA (END)
#                 # RECORD FOUND (END)
#             ### LOOP END
#
#             tracker_gprs_length = TrackerRawData.objects.filter(
#                 vehicle_code_id=ck_vehicle_code,
#                 vendor_date_time__date=dt_start_date
#             ).aggregate(
#                 total_count=Count('id')
#             )['total_count']
#
#             ### UPDATE VEHICLE SCHEDULE GPRS API RECORD
#             UpdateVehiclScheduleGPRSApi = VehicleScheduleGPRSApi.objects.get(
#                 veh_sch_date=dt_start_date,
#                 vehicle_code_id=get_vehicle_id
#             )
#             UpdateVehiclScheduleGPRSApi.retrieve_record = tracker_gprs_length
#
#             if tracker_gprs_length >= total_vendor_record:
#                 UpdateVehiclScheduleGPRSApi.process_status = "Completed"
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
#     django_datetime_from = parse_datetime(get_start_date)
#     django_datetime_to = parse_datetime(get_end_date)
#
#     tracker_raw_gprs_lists = list(TrackerRawData.objects.filter(
#         vehicle_code_id=get_vehicle_id,
#         vendor_date_time__gte=django_datetime_from,
#         vendor_date_time__lte=django_datetime_to
#     ).annotate(
#         x=RawSQL("ST_X(geom)", []),
#         y=RawSQL("ST_Y(geom)", [])
#     ).values("x", "y", "vehicle_code_id", "g_status", "system_date_time", "vendor_date_time", "device_status",
#              "max_speed", "speed", "vehicle_status", "direction", "distance", "mileage"
#              ).order_by('id'))
#
#     ### VEHICLE TRACK CALCULATE LENGTH FROM GPRS DATA
#     VehicleTracks = TrackerRawData.objects.filter(
#         vehicle_code_id=get_vehicle_id,
#         vendor_date_time__gte=django_datetime_from,
#         vendor_date_time__lte=django_datetime_to
#     ).values('vehicle_code_id').annotate(
#         line=MakeLine('geom'),  # Create a line from grouped points
#         length=Length(MakeLine('geom'))  # Calculate line length
#     )
#
#     # Convert data into JSON response
#     VehicleTracks_Length = [
#         {
#             "vehicle_code_id": track["vehicle_code_id"],
#             "length_meters": track["length"].m,  # Convert to meters
#             "line_geojson": track["line"].geojson  # Convert to GeoJSON
#         }
#         for track in VehicleTracks
#     ]
#
#     message = "Success"
#     params = {
#         'message': message,
#         'tracker_raw_gprs_lists': tracker_raw_gprs_lists,
#         'vehicle_tracks_length': VehicleTracks_Length,
#     }
#     logger.info("FetchSingleVehicleTripHistoryData has been executed.")
#     logger.info("-------------------------")
#     return HttpResponse(json.dumps(params, default=date_handler))


# def VehicleRouteReportView(request):
#     template = "Vehicle/VehicleRouteReport11.html"
#     # Get all distinct vehicle types (to always populate the dropdown)
#     vehicle_types = VehicleType.objects.values_list('vehicle_type_name', flat=True).distinct()
#
#     # Get search query and selected vehicle type from GET parameters
#     search_query = request.GET.get('search_vehicle', '')
#     selected_type = request.GET.get('cmd_vehicle_type', 'NA')
#     # Get start and end datetime from GET parameters
#     from_datetime = request.GET.get('from_datetime', '')
#     to_datetime = request.GET.get('to_datetime', '')
#     selected_vehicle_id = request.GET.get('cmd_vehicle_list', 'NA')
#
#     vehicle_ids = []
#     tracker_raw_gprs_lists = []
#     vehicle_tracks_length = []
#     message = ""
#     # If a vehicle type is explicitly selected (not "NA"), filter by type.
#     if selected_type and selected_type != "NA":
#         vehicles = VehicleData.objects.filter(vehicle_type=selected_type)
#         if search_query:
#             vehicles = vehicles.filter(vehicle_code__icontains=search_query)
#         vehicle_ids = vehicles.values_list('vehicle_code', flat=True).distinct()
#     # If no type is selected but a search query is provided, filter on vehicle code
#     elif search_query:
#         vehicle_ids = VehicleData.objects.filter(vehicle_code=search_query) \
#             .values_list('vehicle_code', flat=True) \
#             .distinct()
#
#     # Check if all required parameters are provided to retrieve trip history
#     if from_datetime and to_datetime and selected_vehicle_id != 'NA':
#         # Call the function and extract the JSON data from the response
#         print("Execution the fucntion")
#         logger.info("Sir function is now being executed.")
#         response = FetchSingleVehicleTripHistoryData(selected_vehicle_id, from_datetime, to_datetime)
#         if response:
#             # Parse the JSON content
#             data = json.loads(response.content.decode('utf-8'))
#             tracker_raw_gprs_lists = data.get('tracker_raw_gprs_lists', [])
#             vehicle_tracks_length = data.get('vehicle_tracks_length', [])
#             message = data.get('message', "")
#
#     context = {
#         'vehicle_types': vehicle_types,
#         'vehicle_ids': vehicle_ids,
#         'search_query': search_query,
#         'selected_type': selected_type,
#         'from_datetime': from_datetime,
#         'to_datetime': to_datetime,
#         'selected_vehicle_id': selected_vehicle_id,
#         'tracker_raw_gprs_lists': tracker_raw_gprs_lists,
#         'vehicle_tracks_length': vehicle_tracks_length,
#         'message': message
#     }
#     return render(request, template, context)
