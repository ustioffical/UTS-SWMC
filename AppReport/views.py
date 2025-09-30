import json
from datetime import datetime, timedelta, time

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count

from django.contrib.gis.db.models.aggregates import Collect, MakeLine
from django.contrib.gis.db.models.functions import Length
from django.contrib.gis.db.models import LineStringField
from django.contrib.gis.geos import LineString

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D

from geopy.distance import geodesic

from django.db.models import F

from AppAdmin.utils import *
from AppVehicle.models import *
from AppVehicle.views import *
from VTMS.views import *
from AppSetting.models import TownBoundary


# Create your views here.
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def VehicleRouteReportView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "Vehicle/VehicleRouteReport.html"

    current_data_time = datetime.datetime.now()
    current_date = current_data_time.date()
    format_str_date = "%Y-%m-%d"

    # #### GENERATE GRID FOR VEHICLE DATA TABLE
    # vehicle_type_list = VehicleData.objects.all().order_by('vehicle_type')
    # vehicle_data_obj = []
    # vehicle_distance_summary = [
    #     {'distance_20': 0, 'distance_5': 0, 'distance_less_5': 0}
    # ]
    # for data in vehicle_type_list:
    #     # Set up filters for today's data
    #     tracker_filters = {
    #         'vendor_date_time__date': current_date,
    #         'vehicle_code_id': data.vehicle_code
    #     }
    #
    #     # Get tracker records for this vehicle today
    #     vehicle_tracker_records = TrackerRawData.objects.filter(**tracker_filters).order_by('vendor_date_time')
    #
    #     """
    #     Calculate total distance (in km) for a vehicle on a given date.
    #     Skips records without geometry.
    #     """
    #     round_distance_km = DistanceFinder(vehicle_tracker_records)
    #
    #     """
    #     Calculate total working (in hour) for a vehicle on a given date.
    #     """
    #
    #     fun_working_hours = CalculateSingleVehicleWorkingHour_Function(vehicle_tracker_records)
    #
    #     vehicle_dict = dict()
    #     vehicle_dict["vehicle_code"] = data.vehicle_code
    #     vehicle_dict["pitb_code"] = data.pitb_code
    #     vehicle_dict["register_no"] = data.register_no
    #     vehicle_dict["vehicle_type"] = data.vehicle_type
    #     vehicle_dict["line_length_m"] = f"{(float(round_distance_km) * 1000):.2f}"
    #     vehicle_dict["line_length_km"] = round_distance_km
    #     vehicle_dict["working_hours"] = fun_working_hours
    #
    #     vehicle_data_obj.append(vehicle_dict)
    #
    #     ### GENERATE DISTANCE SUMMARY DICT
    #     distance_km = float(round_distance_km)
    #     if distance_km >= 20:
    #         vehicle_distance_summary[0]['distance_20'] += 1
    #     elif 5 < distance_km < 20:
    #         vehicle_distance_summary[0]['distance_5'] += 1
    #     elif distance_km <= 5:
    #         vehicle_distance_summary[0]['distance_less_5'] += 1
    #     ### GENERATE DISTANCE SUMMARY DICT
    #
    # vehicle_data_obj_sort = sorted(vehicle_data_obj, key=lambda x: float(x['line_length_km']), reverse=True)

    #### GENERATE GRID FOR VEHICLE DATA TABLE

    vehicle_type_list = VehicleData.objects.values('vehicle_type').annotate(count=Count('id')).order_by('vehicle_type')

    ### VEHICLE DATA DETAIL WITH VEHICLE STATUS AND VEHICLE TYPE
    vehicle_data_list = list(
        # VehicleData.objects.filter(**filters_vehicle_data)
        VehicleData.objects.values('vehicle_code', 'vehicle_type', 'register_no', 'chasis_no')
        .annotate(
            pitb_code=Coalesce('pitb_code', Value('Waiting'), output_field=CharField())
        )
        .order_by('register_no')
        .distinct()
    )

    ### ASSET TYPE SUMMARY WITH COUNT
    query_asset_type = "SELECT 'Container' as name, count(*) AS value FROM tbl_container_data UNION ALL SELECT 'Drum' as name, count(*) AS value FROM tbl_drum_data UNION ALL SELECT 'Collection-Site' as name, count(*) AS value FROM tbl_collection_site UNION ALL SELECT 'Dumping-Site' as name, count(*) AS value FROM tbl_dumping_site UNION ALL SELECT 'Landuse' as name, count(*) AS value FROM tbl_landuse_boundary UNION ALL SELECT 'Admin' as name, count(*) AS value FROM tbl_administrative_boundary; ";
    cursor.execute(query_asset_type)
    asset_type_summary = DictinctFetchAll(cursor)
    #
    ### VEHICLE LIVE MONITORING DATA
    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, chasis_no, register_no, vehicle_type, g_status, direction, speed, COALESCE(device_status, 'NA') AS device_status, COALESCE(ignition_status, 'NA') AS ignition_status, COALESCE(geo_location, 'NA') AS geo_location, vendor_date_time, COALESCE(duration, 'NA') AS duration FROM tbl_vehicle_live_monitor AS vlm LEFT OUTER JOIN tbl_vehicle_data AS veh ON vlm.vehicle_code_id = veh.vehicle_code; ";
    cursor.execute(query_feature)
    vehicle_live_lists = DictinctFetchAll(cursor)

    page_title = "Report Vehicle"
    params = {
        # 'vehicle_distance_summary': vehicle_distance_summary[0],
        # 'vehicle_data_obj': vehicle_data_obj_sort,
        'vehicle_type_list': vehicle_type_list,
        'vehicle_data_list': vehicle_data_list,
        'asset_type_summary': asset_type_summary,
        'vehicle_live_lists': vehicle_live_lists,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


def VehicleHistoryReportView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "Vehicle/VehicleHistory.html"

    ### VEHICLE TRACK CALCULATE LENGTH FROM GPRS DATA
    VehicleTracks = TrackerRawData.objects.values('vehicle_code_id').annotate(
        line=MakeLine('geom'),  # Create a line from grouped points
        length=Length(MakeLine('geom'))  # Calculate line length
    )

    # Convert data into JSON response
    VehicleTracks_Length = [
        {
            "vehicle_code_id": track["vehicle_code_id"],
            "length_meters": track["length"].m,  # Convert to meters
            "line_geojson": track["line"].geojson  # Convert to GeoJSON
        }
        for track in VehicleTracks
    ]

    vehicle_type_list = VehicleData.objects.all().order_by('vehicle_type')

    #### GENERATE GRID FOR VEHICLE DATA TABLE

    vehicle_data_obj = []
    for data in vehicle_type_list:
        vehicle_dict = dict()
        vehicle_dict["vehicle_code"] = data.vehicle_code
        vehicle_dict["register_no"] = data.register_no
        vehicle_dict["vehicle_type"] = data.vehicle_type
        vehicle_dict["line_length_m"] = 0
        vehicle_dict["line_length_km"] = 0

        for l in range(int(len(VehicleTracks_Length))):
            len_vehicle_code_id = VehicleTracks_Length[l]['vehicle_code_id']

            if data.vehicle_code == len_vehicle_code_id:
                vehicle_dict["line_length_m"] = f"{VehicleTracks_Length[l]['length_meters']:.2f}"
                vehicle_dict["line_length_km"] = f"{(float(VehicleTracks_Length[l]['length_meters']) / 1000):.2f}"

        vehicle_data_obj.append(vehicle_dict)

    vehicle_data_obj_sort = sorted(vehicle_data_obj, key=lambda x: float(x['line_length_km']), reverse=True)

    #### GENERATE GRID FOR VEHICLE DATA TABLE

    vehicle_type_data_list = list(
        VehicleData.objects.values('vehicle_type').annotate(count=Count('id')).order_by('vehicle_type'))

    ### ASSET TYPE SUMMARY WITH COUNT
    query_asset_type = "SELECT 'Container' as name, count(*) AS value FROM tbl_container_data UNION ALL SELECT 'Drum' as name, count(*) AS value FROM tbl_drum_data UNION ALL SELECT 'Collection-Site' as name, count(*) AS value FROM tbl_collection_site UNION ALL SELECT 'Dumping-Site' as name, count(*) AS value FROM tbl_dumping_site UNION ALL SELECT 'Landuse' as name, count(*) AS value FROM tbl_landuse_boundary UNION ALL SELECT 'Admin' as name, count(*) AS value FROM tbl_administrative_boundary; ";
    cursor.execute(query_asset_type)
    asset_type_summary = DictinctFetchAll(cursor)

    ### VEHICLE LIVE MONITORING DATA
    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, chasis_no, register_no, vehicle_type, g_status, direction, speed, COALESCE(device_status, 'NA') AS device_status, COALESCE(ignition_status, 'NA') AS ignition_status, COALESCE(geo_location, 'NA') AS geo_location, vendor_date_time, COALESCE(duration, 'NA') AS duration FROM tbl_vehicle_live_monitor AS vlm LEFT OUTER JOIN tbl_vehicle_data AS veh ON vlm.vehicle_code_id = veh.vehicle_code; ";
    cursor.execute(query_feature)
    vehicle_live_lists = DictinctFetchAll(cursor)

    page_title = "Report Vehicle"
    params = {
        'vehicle_type_list': vehicle_type_data_list,
        'vehicle_data_obj': vehicle_data_obj_sort,
        'vehicle_tracks_length': VehicleTracks_Length,
        'asset_type_summary': asset_type_summary,
        'vehicle_live_lists': vehicle_live_lists,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


def VehicleTripHistoryReportView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "Vehicle/VehicleTripHistory.html"

    current_data_time = datetime.datetime.now()
    current_date = current_data_time.date()
    format_str_date = "%Y-%m-%d"
    work_date_str = (current_date - timedelta(days=2)).strftime(format_str_date)

    ### SYNC TRACKER GPRS VEHICLE DATA BY VENDOR SYSTEM
    # SyncTrackerGPRSVehicleData_By_Vendor_Function('278909', '2025-05-08')

    # UTSPostVTMSBulk(279204, '2025-05-07')
    # UTSPostVTMSLoop(278909, '2025-04-30')
    # UTSPostVTMS(278909, '2025-04-29')

    # UTSPostVTMSBulkBackend_2Min()

    #### GENERATE GRID FOR VEHICLE DATA TABLE
    vehicle_type_list = VehicleData.objects.all().order_by('vehicle_type')
    vehicle_data_obj = []
    for data in vehicle_type_list:

        vehicle_code = data.vehicle_code

        points = TrackerRawData.objects.filter(
            vehicle_code_id=vehicle_code,
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

        vehicle_dict = dict()
        vehicle_dict["vehicle_code"] = data.vehicle_code
        vehicle_dict["register_no"] = data.register_no
        vehicle_dict["vehicle_type"] = data.vehicle_type
        vehicle_dict["line_length_m"] = total_distance
        vehicle_dict["line_length_km"] = f"{(float(total_distance) / 1000):.2f}"

        vehicle_data_obj.append(vehicle_dict)

    vehicle_data_obj_sort = sorted(vehicle_data_obj, key=lambda x: float(x['line_length_km']), reverse=True)

    #### GENERATE GRID FOR VEHICLE DATA TABLE

    vehicle_type_data_list = list(
        VehicleData.objects.values('vehicle_type').annotate(count=Count('id')).order_by('vehicle_type'))

    ### ASSET TYPE SUMMARY WITH COUNT
    query_asset_type = "SELECT 'Container' as name, count(*) AS value FROM tbl_container_data UNION ALL SELECT 'Drum' as name, count(*) AS value FROM tbl_drum_data UNION ALL SELECT 'Collection-Site' as name, count(*) AS value FROM tbl_collection_site UNION ALL SELECT 'Dumping-Site' as name, count(*) AS value FROM tbl_dumping_site UNION ALL SELECT 'Landuse' as name, count(*) AS value FROM tbl_landuse_boundary UNION ALL SELECT 'Admin' as name, count(*) AS value FROM tbl_administrative_boundary; ";
    cursor.execute(query_asset_type)
    asset_type_summary = DictinctFetchAll(cursor)
    #
    ### VEHICLE LIVE MONITORING DATA
    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, chasis_no, register_no, vehicle_type, g_status, direction, speed, COALESCE(device_status, 'NA') AS device_status, COALESCE(ignition_status, 'NA') AS ignition_status, COALESCE(geo_location, 'NA') AS geo_location, vendor_date_time, COALESCE(duration, 'NA') AS duration FROM tbl_vehicle_live_monitor AS vlm LEFT OUTER JOIN tbl_vehicle_data AS veh ON vlm.vehicle_code_id = veh.vehicle_code; ";
    cursor.execute(query_feature)
    vehicle_live_lists = DictinctFetchAll(cursor)

    page_title = "Report Vehicle"
    params = {
        'vehicle_data_obj': vehicle_data_obj_sort,
        'vehicle_type_list': vehicle_type_data_list,
        'asset_type_summary': asset_type_summary,
        'vehicle_live_lists': vehicle_live_lists,
        'page_title': page_title,
        'message': message,
    }

    return render(request, template_name, params)


def ContainerHistoryReportView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "Container/ContainerHistory.html"

    # ### VEHICLE TRACK CALCULATE LENGTH FROM GPRS DATA
    # VehicleTracks = TrackerRawData.objects.values('vehicle_code_id').annotate(
    #     line=MakeLine('geom'),  # Create a line from grouped points
    #     length=Length(MakeLine('geom'))  # Calculate line length
    # )
    #
    # # Convert data into JSON response
    # VehicleTracks_Length = [
    #     {
    #         "vehicle_code_id": track["vehicle_code_id"],
    #         "length_meters": track["length"].m,  # Convert to meters
    #         "line_geojson": track["line"].geojson  # Convert to GeoJSON
    #     }
    #     for track in VehicleTracks
    # ]
    #
    # vehicle_type_list = VehicleData.objects.all().order_by('vehicle_type')
    #
    # #### GENERATE GRID FOR VEHICLE DATA TABLE
    #
    # vehicle_data_obj = []
    # for data in vehicle_type_list:
    #     vehicle_dict = dict()
    #     vehicle_dict["vehicle_code"] = data.vehicle_code
    #     vehicle_dict["register_no"] = data.register_no
    #     vehicle_dict["vehicle_type"] = data.vehicle_type
    #     vehicle_dict["line_length_m"] = 0
    #     vehicle_dict["line_length_km"] = 0
    #
    #     for l in range(int(len(VehicleTracks_Length))):
    #         len_vehicle_code_id = VehicleTracks_Length[l]['vehicle_code_id']
    #
    #         if data.vehicle_code == len_vehicle_code_id:
    #             vehicle_dict["line_length_m"] = f"{VehicleTracks_Length[l]['length_meters']:.2f}"
    #             vehicle_dict["line_length_km"] = f"{(float(VehicleTracks_Length[l]['length_meters']) / 1000):.2f}"
    #
    #     vehicle_data_obj.append(vehicle_dict)
    #
    # vehicle_data_obj_sort = sorted(vehicle_data_obj, key=lambda x: float(x['line_length_km']), reverse=True)
    #
    # #### GENERATE GRID FOR VEHICLE DATA TABLE
    #
    # vehicle_type_list = VehicleType.objects.all().order_by('vehicle_type_name')
    #
    # # query_container_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, container_code, container_name, status FROM tbl_container_data WHERE status = 'Active'; "
    # # cursor.execute(query_container_feature)
    # # container_feature = DictinctFetchAll(cursor)
    # # #
    # # town_boundary = TownBoundary.objects.all().order_by('town_name')
    #
    query_container_feature = "WITH cp AS (SELECT container_code_id, check_in, check_out, net_time_spent, cont_proc_type_code_id, vehicle_code_id FROM tbl_container_process WHERE created_at::date = '2025-02-26') SELECT container_code_id, container_name, check_in, check_out, net_time_spent, cont_proc_type_code_id, cont_proc_type_name, vehicle_code_id, register_no, vehicle_type FROM cp INNER JOIN tbl_container_process_type ct ON cp.cont_proc_type_code_id = ct.cont_proc_type_code INNER JOIN tbl_container_data cd ON cp.container_code_id = cd.container_code INNER JOIN tbl_vehicle_data veh ON cp.vehicle_code_id = veh.vehicle_code "
    cursor.execute(query_container_feature)
    container_process_data = DictinctFetchAll(cursor)

    complete_container_detail = [{
        'name': 'Visited',
        'data': [16],
        'color': '#96CC39',
        'pointWidth': 50
    }, {
        'name': 'Not Visited',
        'data': [72],
        'color': 'orange',
        'pointWidth': 50
    }]

    TownWiseDetail = [{
        'name': 'Visited',
        'data': [34, 39, 53, 56],
        'color': '#96CC39'
    }, {
        'name': 'Not Visited',
        'data': [27, 21, 22, 78],
        'color': 'orange'
    }]

    town_names = ['Ali Town', 'Gulberg Town', 'Awan Town', 'Naseem Town']

    page_title = "Report Container"
    params = {
        'container_process_data': container_process_data,
        # 'vehicle_data_obj': vehicle_data_obj_sort,
        # 'vehicle_tracks_length': VehicleTracks_Length,
        'page_title': page_title,
        'complete_container_detail': complete_container_detail,
        'TownWiseDetail': TownWiseDetail,
        'town_names': town_names,
        'message': message,
    }

    return render(request, template_name, params)
