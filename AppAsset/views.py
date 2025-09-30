import json
import datetime
import requests

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from AppAdmin.utils import *
from AppAsset.serializers import *
from AppAsset.forms import *
from django.shortcuts import get_object_or_404
from AppVehicle.models import VehicleData,TrackerRawData,VehicleScheduleGPRSApi
from AppVehicle.views import ResponseTrackerGPRSRawApi_By_Vendor_Function,SyncTrackerGPRSVehicleData_By_Vendor_Function
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def ContainerListView(request):
    message = ""
    cursor = connections['default'].cursor()
    template_name = "Container/ContainerList.html"

    container_list = ContainerData.objects.all().order_by('mc_code',
                                                          'container_name')

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, container_code, container_name, status FROM tbl_container_data WHERE status = 'Active' ";
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    town_boundary = TownBoundary.objects.all().order_by('town_name')

    params = {
        'container_list': container_list,
        'town_boundary': town_boundary,
        'feature_lists': feature_lists,
        'message': message,
    }

    return render(request, template_name, params)


def CreateContainerView(request):
    # employee_count = EmployeeInformation.objects.all().count()
    message = ""
    template_name = "Container/Create.html"
    # dateTime = datetime.datetime.now()
    #
    # format_str = '"%Y-%m-%d %H:%M:%S"'
    # today_date = dateTime.strftime(format_str)

    breadcrumb_list = []
    breadcrumb_dict = dict()
    breadcrumb_dict["hire_date"] = "Container"

    auto_container_code = AutoGenerateCodeForModel(ContainerData, "container_code", "CNT-")

    form = FormContainer()
    if request.method == "POST":
        form_class = FormContainer(request.POST, request.FILES)

        if form_class.is_valid():
            get_form_inst = form_class.save(commit=False)

            get_form_inst.container_code = auto_container_code

            get_feature_coordinate = request.POST['feature_coordinate']
            get_latitude = request.POST['lattitude']
            get_longitude = request.POST['longitude']

            get_form_inst.longitude = get_latitude
            get_form_inst.latitude = get_longitude
            get_form_inst.geom = get_feature_coordinate

            get_mc = request.POST['cmd_mc']
            get_install_year = request.POST['install_year']

            get_form_inst.mc_code_id = get_mc
            get_form_inst.install_year = get_install_year

            get_form_inst.save()

        message = "Success"
    else:
        form = FormContainer()

    town_boundary = TownBoundary.objects.all().order_by('town_name')

    params = {
        #     'employee_user_role': employee_user_role,
        'auto_container_code': auto_container_code,
        'form': form,
        'town_boundary': town_boundary,
        #     'position_list': position_list,
        #     'payment_list': payment_list,
        #     'location_store_list': location_store_list,
        'message': message,
        #     ' employee_count': employee_count,
        #     'working_schedule_list': working_schedule_list,
    }

    return render(request, template_name, params)


# AJAX
def FetchDrumFeatureDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, drum_code, drum_name, status FROM tbl_drum_data WHERE status = 'Active' ";
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchContainerFeatureDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, container_code, container_name, status FROM tbl_container_data WHERE status = 'Active' ";
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchContainerFeatureData_ProcessTypeView(request):
    cursor = connections['default'].cursor()

    query_feature = "WITH process AS ( SELECT DISTINCT container_code_id, cont_proc_type_code_id, cont_proc_type_name FROM tbl_container_process AS cp INNER JOIN tbl_container_process_type AS cpt ON cp.cont_proc_type_code_id = cpt.cont_proc_type_code WHERE cp.created_at::date BETWEEN '2025-02-26' AND '2025-02-27' GROUP BY container_code_id, cont_proc_type_code_id, cont_proc_type_name ) SELECT container_code_id, cont_proc_type_code_id, cont_proc_type_name, ST_X(geom) as x, ST_Y(geom) as y, container_name FROM process INNER JOIN tbl_container_data AS cd ON process.container_code_id = cd.container_code WHERE cd.status = 'Active' ORDER BY SPLIT_PART(container_code_id, '-', 2)::INTEGER, cont_proc_type_name ; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchDumpingSiteDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, code, name, status FROM tbl_dumping_site "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchDumpingCoverageDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from (SELECT geom, code, dump_site_code_id FROM tbl_dumping_coverage ) as foo) As f )  As fc; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchWeighingSiteDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, weigh_code AS code, weigh_name AS name, status FROM tbl_weighing_site "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchWeighingCoverageDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT row_to_json(fc) geojson FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, st_asgeojson(ST_Transform(geom,4326))::json  As geometry, row_to_json((SELECT l FROM (select foo.*) as l ))as properties from (SELECT geom, code, weigh_code_id FROM tbl_weighing_coverage ) as foo) As f )  As fc; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchCollectionSiteDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, tcp_code AS code, tcp_name AS name, status FROM tbl_collection_site; "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchParkingSiteDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, code, name, status FROM tbl_parking_site "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchWorkshopDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, code, name, status FROM tbl_workshop "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


def FetchFillingStationDataView(request):
    cursor = connections['default'].cursor()

    query_feature = "SELECT ST_X(geom) as x, ST_Y(geom) as y, code, name, status FROM tbl_filling_station "
    cursor.execute(query_feature)
    feature_lists = DictinctFetchAll(cursor)

    message = "Success"
    params = {
        'message': message,
        'feature_lists': feature_lists,
    }

    return HttpResponse(json.dumps(params, default=date_handler))


# For disaplying and compairing vehicle last location
def VehicleLastLocationView(request):
    template_name = "Container/VehicleLastLocation.html"
    vehicle_code = request.POST.get('vehicle_code')
    vehicle_codes = VehicleData.objects.all().order_by('vehicle_code')
    message = ""
    context = {
        'vehicle_codes': vehicle_codes,
        'message': message,
    }
    tracker_data = TrackerRawData.objects.filter(vehicle_code=vehicle_code,
                                                 vendor_date_time__date=datetime.datetime.now().date()).order_by(
        '-vendor_date_time').exists()
    if vehicle_code and tracker_data:
        # First getting the vehicle latest location from DB TrackerRawData
        vehicle = get_object_or_404(VehicleData, vehicle_code=vehicle_code)
        uts_last_location = TrackerRawData.objects.filter(vehicle_code=vehicle.vehicle_code,
                                                          vendor_date_time__date=datetime.datetime.now().date()).order_by(
            '-vendor_date_time').first()
        if uts_last_location:
            logger.info(
                f"DB Last Location: lat={uts_last_location.latitude}, lon={uts_last_location.longitude}, time={uts_last_location.vendor_date_time}")
        uts_last_location_time = uts_last_location.vendor_date_time.strftime("%Y-%m-%d %H:%M:%S")
        uts_last_location_longitude = uts_last_location.longitude
        uts_last_location_latitude = uts_last_location.latitude
        # Now getting the last location from vendor API
        get_selected_date = datetime.datetime.now().strftime("%Y-%m-%d")
        logger.info("Selected Date: " + str(get_selected_date))
        get_from_time = "00:00:00"
        get_to_time = "23:59:59"

        ### COMBINE DATE AND TIME INTO STRING
        datetime_from = get_selected_date + " " + get_from_time
        datetime_to = get_selected_date + " " + get_to_time

        vendor_json = ResponseTrackerGPRSRawApi_By_Vendor_Function(vehicle_code, datetime_from, datetime_to)

        if vendor_json:
            vehicle_gprs_response_api = vendor_json['Table']
        else:
            vehicle_gprs_response_api = []
        vendor_last_location = vehicle_gprs_response_api[len(vehicle_gprs_response_api) - 1]
        vendor_last_location_longitude = vendor_last_location['Long']
        vendor_last_location_latitude = vendor_last_location['Lat']
        vendor_last_location_time = vendor_last_location['GpsTime'].replace('T', ' ')
        logger.info(f"Length of vendor API {len(vehicle_gprs_response_api[-1])}")
        logger.info(json.dumps(vehicle_gprs_response_api[-1], indent=4))
        # Convert times to datetime objects for subtraction
        try:
            vendor_last_location_dt = datetime.datetime.strptime(vendor_last_location_time, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            vendor_last_location_dt = datetime.datetime.strptime(vendor_last_location_time, "%Y-%m-%d %H:%M:%S")
        uts_last_location_dt = datetime.datetime.strptime(uts_last_location_time, "%Y-%m-%d %H:%M:%S")
        # Now finding time difference
        time_difference = vendor_last_location_dt - uts_last_location_dt
        logger.info(f"Time Difference: {time_difference}")
        time_difference_minutes = round(time_difference.total_seconds() / 60, 2)
        logger.info(f"Time Difference: {time_difference_minutes} minutes")
        color = "red"
        if time_difference_minutes < 60:
            logger.warning(f"Time difference is more than 60 minutes: {time_difference_minutes} minutes")
            color = "green"
        # Getting the distance and Working Hour
        vehicle_schedule = VehicleScheduleGPRSApi.objects.filter(vehicle_code=vehicle_code,
                                                                 veh_sch_date=datetime.datetime.now().date()).first()
        if vehicle_schedule:
            distance = vehicle_schedule.distance
            working_hour = vehicle_schedule.working_hours
            logger.info(f"Distance: {distance} km, Working Hour: {working_hour} hours")
        else:
            distance = 0
            working_hour = 0
            logger.info("No schedule data available for this vehicle today")
        # Now if We press sunc button then we wil sync data
        if request.method == 'POST' and 'sync_data' in request.POST:
            sync_response = SyncTrackerGPRSVehicleData_By_Vendor_Function(vehicle_code, datetime_from, datetime_to)
            if sync_response:
                logger.info(f"Sync Response: {sync_response}")
                message = "Data Synced Successfully"
            else:
                message = "No Data to Sync"

        context.update({
            'vehicle_codes': vehicle_codes,
            'uts_last_location_time': uts_last_location_time,
            'uts_last_location_longitude': uts_last_location_longitude,
            'uts_last_location_latitude': uts_last_location_latitude,
            'vendor_last_location_time': vendor_last_location_time,
            'vendor_last_location_longitude': vendor_last_location_longitude,
            'vendor_last_location_latitude': vendor_last_location_latitude,
            'time_difference_minutes': time_difference_minutes,
            'distance': distance,
            'working_hour': working_hour,
            'color': color,
            'message': message,
        })
    else:
        message = "No vendor data available for this vehicle"
        context['message'] = message

    return render(request, template_name, context)
