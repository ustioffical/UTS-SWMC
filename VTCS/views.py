from django.shortcuts import render, get_object_or_404
import requests
from .models import *
from rest_framework import viewsets
from .serializers import *
import os
from .models import *
from .forms import *
from django.db import transaction
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import APITripDataFilter
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import APITripData
from AppVehicle.models import VehicleData, TrackerRawData
from django.http import JsonResponse
from AppAsset.models import *
from django.db.models import Q
import json
from AppAdmin.utils import *

from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Sum

AUTH_KEY = os.environ.get('AUTH_KEY')


class PostTripDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = APITripData.objects.all()
    serializer_class = PostTripDataSerializer


# VTCSTripList.html is related to this viewset
class ViewVTCSTripDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch']
    serializer_class = ViewTripDataSerializer
    queryset = APITripData.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = APITripDataFilter
    search_fields = ['vehicle_code', 'tms_code', 'site_name', 'response_id']

    # @transaction.atomic
    # def partial_update(self, request, *args, **kwargs):
    #
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # Save the serializer inside the transaction
    #     updated_instance = serializer.save()
    #
    #     # If there's a response_id, update PITB
    #     if updated_instance.response_id:
    #         result = UpdateVTCSPITBAPIByDataId(updated_instance.response_id)
    #         if result["status_code"] not in [200, 201]:
    #             # Raise an exception to trigger rollback
    #             raise Exception(f"PITB update failed: {result['status_code']} - {result['response_data']}")
    #     else:
    #         # If there is no response_id then post the local data to PITB-VTCS API
    #         result = PostVTCSToPITBAPIById(updated_instance.id)
    #         if result["status_code"] not in [200, 201]:
    #             # Raise an exception to trigger rollback
    #             raise Exception(f"PITB API submission failed: {result['status_code']} - {result['response_data']}")
    #
    #     # Return the updated instance
    #     return Response(serializer.data)


# Sperate function and view for Pushing data to PITB API for POST and Update Request

def push_trip_data_view(request):
    if request.method == "POST":
        trip_id = request.POST.get('trip_id')

        # Debug to check what's in the request
        print(f"Received request: POST data: {request.POST}")

        if not trip_id:
            # Try also checking in the request body
            try:
                import json
                data = json.loads(request.body)
                trip_id = data.get('trip_id')
            except:
                # Still no trip_id found
                pass

        if not trip_id:
            return JsonResponse({
                "status_code": 400,
                "response_data": "Missing trip_id parameter"
            })

        # Call your existing PushDataToPITBAPI function
        result = PushDataToPITBAPI(trip_id)
        return JsonResponse(result)

    return JsonResponse({
        "status_code": 405,
        "response_data": "Method not allowed"
    })


def PushDataToPITBAPI(trip_id):
    # Fist checking if response_id is present in the trip data
    trip_data = get_object_or_404(APITripData, id=trip_id)
    if trip_data.response_id:
        # If response_id is present then update the data in PITB API
        result = UpdateVTCSPITBAPIByDataId(trip_data.response_id)
        # result={"status_code":200,"response_data":"Pushed to PITB"}
        return result
    else:
        # If response_id is not present then post the local data to PITB-VTCS API
        # result={"status_code":200,"response_data":"Pushed to PITB"}
        result = PostVTCSToPITBAPIById(trip_id)
        return result

from datetime import datetime, timedelta
@login_required(login_url='LoginView')
# For displaying the Trip List HTML page
def ViewVTCSTripDataList(request):
    template_name = "PITBApi/VTCSTripList.html"

    format_date = '%Y-%m-%d'
    current_data_time = datetime.now()
    today_date = current_data_time.strftime(format_date)
    cursor = connections['default'].cursor()

    # Initialize filter parameters
    selected_vehicle_type = "NA"
    selected_vehicle_code = "NA"
    selected_response_status = "NA"
    trip_start_date = today_date
    trip_end_date = today_date

    # Get filter parameters from either GET or POST
    if request.method == "POST":
        selected_vehicle_type = request.POST.get('vehicle_type', 'NA')
        selected_vehicle_code = request.POST.get('vehicle_code', 'NA')
        selected_response_status = request.POST.get('response_status', 'NA')
        trip_start_date = request.POST.get('trip_start_date', today_date)
        trip_end_date = request.POST.get('trip_end_date', today_date)

    # Create base queryset - MOVED AFTER parameter processing
    api_trip_list = APITripData.objects.defer('gprs_raw_code').filter(
        vehicle_code__vehicle_type__in=['Dumper 10m3', 'Dumper 5m3']
    )

    # Apply date filter
    if trip_start_date and trip_end_date:
        api_trip_list = api_trip_list.filter(trip_date__range=[trip_start_date, trip_end_date])
    else:
        api_trip_list = api_trip_list.filter(trip_date__gte=datetime.now().date() - timedelta(days=1))

    # Order by trip_date
    api_trip_list = api_trip_list.order_by('-trip_date')

    # Apply other filters
    if selected_vehicle_type != "NA":
        api_trip_list = api_trip_list.filter(vehicle_code__vehicle_type=selected_vehicle_type)

    if selected_vehicle_code != "NA":
        api_trip_list = api_trip_list.filter(vehicle_code__pitb_code=selected_vehicle_code)

    if selected_response_status != "NA":
        if selected_response_status == "Waiting":
            api_trip_list = api_trip_list.filter(Q(response_status__isnull=True) | Q(response_status=""))
        else:
            api_trip_list = api_trip_list.filter(response_status=selected_response_status)

    # Rest of the function remains the same
    completed_count = APITripData.objects.filter(response_status="Success").count()
    pending_count = APITripData.objects.filter(~Q(response_status="Success")).count()

    vehicle_type_list = VehicleData.objects.filter(
        vehicle_type__in=['Dumper 10m3', 'Dumper 5m3']
    ).values('vehicle_type').annotate(count=Count('id')).order_by('vehicle_type')

    vehicles_data_list = VehicleData.objects.filter(
        pitb_code__isnull=False,
        vehicle_type__in=['Dumper 10m3', 'Dumper 5m3']
    ).values(
        'pitb_code',
        'register_no'
    ).order_by('register_no')

    api_trip_data_list = APITripData.objects.values('response_status').annotate(
        count=Count('id')
    ).order_by('response_status')

    vehicle_count = VehicleData.objects.count()

    # Replace None with "waiting"
    for trip in api_trip_data_list:
        if trip['response_status'] is None or trip['response_status'] == "":
            trip['response_status'] = "Waiting"

    # Use the same date filter for weight calculations
    date_filter = {}
    if trip_start_date and trip_end_date:
        date_filter = {'trip_date__range': [trip_start_date, trip_end_date]}
    else:
        date_filter = {'trip_date__gte': datetime.now().date() - timedelta(days=1)}

    # Calculate total weight and net weight with the same date filter
    total_weight = APITripData.objects.filter(**date_filter).aggregate(total=Sum('before_weight'))
    net_weight = APITripData.objects.filter(**date_filter).aggregate(
        net=Sum('before_weight') - Sum('after_weight')
    )

    # Apply the same date filter to graph data
    graph_data = APITripData.objects.values('vehicle_code__pitb_code').annotate(
        total_before_weight=Sum('before_weight'),
        total_after_weight=Sum('after_weight'),
        net_weight=Sum('before_weight') - Sum('after_weight'),
        trip_count=Count('id')
    ).filter(**date_filter)

    params = {
        'today_date': today_date,
        'vehicle_type_list': vehicle_type_list,
        'api_trip_data_list': api_trip_data_list,
        'vehicle_count': vehicle_count,
        'api_trip_list': api_trip_list,
        'vehicles_data_list': vehicles_data_list,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'selected_vehicle_type': selected_vehicle_type,
        'selected_vehicle_code': selected_vehicle_code,
        'selected_response_status': selected_response_status,
        'trip_start_date': trip_start_date,
        'trip_end_date': trip_end_date,
        'total_weight': total_weight['total'],
        'net_weight': net_weight['net'],
        'graph_data': json.dumps(list(graph_data))
    }

    return render(request, template_name, params)


# This Viewset below is only for posting Trip Data Form in VehicleTripAPIVTCSpost.html
# This view will save data in local db and PITB API
def vehicletripvtcs(request):
    vehicles_data_list = VehicleData.objects.filter(pitb_code__isnull=False,
                                                    vehicle_type="Dumper 10m3").only(
        'vehicle_code',
        'pitb_code',
        'register_no').order_by(
        'register_no')

    # Initialize empty form for GET requests
    if request.method == "GET":
        form = VTCSForm()
    elif request.method == "POST":
        form = VTCSForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Get GPRS data if available
                gprs = None
                try:
                    gprs_obj = TrackerRawData.objects.first()
                    if gprs_obj:
                        gprs = gprs_obj.gprs_raw_code
                except TrackerRawData.DoesNotExist:
                    pass

                # Create but don't save the trip object yet
                trip = form.save(commit=False)
                trip.gprs_raw_code = gprs
                trip.save()

                messages.success(request, "Trip data saved successfully.")

                # Determine which button was clicked using the 'action' parameter
                action = request.POST.get("action", "save")
                if action == "push":
                    # Get the ID of the newly created trip and send to PITB API
                    trip_id = trip.id
                    api_response = PostVTCSToPITBAPIById(trip_id)
                    if api_response["status_code"] in [200, 201]:
                        messages.success(request, f"Pushed to PITB system")
                    elif api_response.get("already_sent", False):
                        messages.info(request, "Trip data was already sent to PITB API.")
                    else:
                        messages.warning(request,
                                         f"Trip data saved but failed to push to PITB server: {api_response['response_data']}")
                else:
                    # This is for the "Save in System" button (action="save")
                    messages.info(request, "Trip data saved locally only.")

                # Redirect to same page with a fresh form after successful submission
                return redirect("vehicletripvtcs")

            except Exception as e:
                messages.error(request, f"Error saving trip: {str(e)}")
        else:
            # If form is invalid, show validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {
        'form': form,
        'vehicles_data_list': vehicles_data_list,

    }
    return render(request, "PostVTCSForm.html", context)


# PITB Data send by using id only

def PostVTCSToPITBAPIById(VTCS_id):
    try:
        # Find trips for this vehicle on this date
        vehicle_data = APITripData.objects.filter(
            id=VTCS_id
        ).first()
        print(f"Processing trip ID: {VTCS_id}, Found data: {vehicle_data is not None}")
        if not vehicle_data:
            return {
                "status_code": 404,
                "response_data": f"No trip data found for vehicle {VTCS_id}"
            }
        if vehicle_data.response_status == "Success":
            return {
                "status_code": 200,
                "response_data": f"Data for vehicle {VTCS_id} was already successfully sent to PITB",
                "already_sent": True
            }
            # Prepare the base data without image fields
        extracted_data = {
            "vehicle_no": str(vehicle_data.vehicle_code),
            "before_weight": float(vehicle_data.before_weight),
            "after_weight": float(vehicle_data.after_weight),
            "time_in": vehicle_data.time_in.strftime('%Y-%m-%d %H:%M:%S'),
            "time_out": vehicle_data.time_out.strftime('%Y-%m-%d %H:%M:%S'),
            "slip_id": str(vehicle_data.slip_id),
            "lat": float(vehicle_data.lat),
            "long": float(vehicle_data.long),
            "site_name": str(vehicle_data.site_name),
            "site_id": str(vehicle_data.site_id),
        }

        # Prepare files for multipart upload - these are required fields
        files = {}

        # Handle required image fields
        if vehicle_data.before_picture:
            files['before_picture'] = (
                vehicle_data.before_picture.name,
                vehicle_data.before_picture.file,
                'image/jpeg'  # Adjust content type based on actual file type
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required before_picture"
            }

        if vehicle_data.after_picture:
            files['after_picture'] = (
                vehicle_data.after_picture.name,
                vehicle_data.after_picture.file,
                'image/jpeg'  # Adjust content type based on actual file type
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required after_picture"
            }

        # Handle optional image fields
        if vehicle_data.roof_before_picture:
            files['roof_before_picture'] = (
                vehicle_data.roof_before_picture.name,
                vehicle_data.roof_before_picture.file,
                'image/jpeg'
            )

        if vehicle_data.roof_after_picture:
            files['roof_after_picture'] = (
                vehicle_data.roof_after_picture.name,
                vehicle_data.roof_after_picture.file,
                'image/jpeg'
            )

        api_url = "https://elgcd-ms.punjab.gov.pk/api/vtcs/post-trip-data"

        headers = {
            'accept': 'application/json',
            'authkey': 'SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1',
            # 'Content-Type': 'multipart/form-data'
        }

        try:
            response = requests.post(
                url=api_url,
                headers=headers,
                data=extracted_data,
                files=files,  # This will handle the multipart/form-data format correctly
                timeout=30
            )

            # Handle response
            response_data = None
            try:
                response_data = response.json() if response.status_code in [200, 201] else response.text
            except ValueError:
                response_data = response.text

            # Update the APITripData record with the response information
            if response.status_code in [200, 201]:
                # Check if we have json data
                if isinstance(response_data, dict):
                    # Extract data_id from response if available
                    data_id = response_data.get('data_id')
                    message = response_data.get('message', '')
                    # Debug before update
                    print(f"Before update: status={vehicle_data.response_status}, id={vehicle_data.response_id}")

                    # Update record fields
                    vehicle_data.response_id = data_id
                    vehicle_data.response_status = "Success"
                    vehicle_data.remarks = message
                    # Debug after field assignment but before save
                    print(f"Assigned values: id={data_id}, status=Success, remarks={message}")
                    vehicle_data.save()
                    # Debug after save
                    print(f"After save: status={vehicle_data.response_status}, id={vehicle_data.response_id}")
                else:
                    # Handle error case
                    vehicle_data.response_status = "Rejected"
                    vehicle_data.remarks = str(response_data)
                    vehicle_data.save()
            # First Checking if the trip data is already in ApiTripDataLogs
            trip_data_logs = ApiTripDataLogs.objects.filter(trip_data_id=vehicle_data.id).first()
            # if exists then update the trip data logs
            if trip_data_logs:
                trip_data_logs.hit_count += 1
                trip_data_logs.current_response = response_data
                trip_data_logs.save()
            else:
                # Also Adding data in VTCS ApiTripDataLogs

                ApiTripDataLogs.objects.create(
                    trip_data_id=vehicle_data,
                    current_response=response_data,
                    hit_count=1,
                )
            return {
                "status_code": response.status_code,
                "response_data": response_data,
            }
        except requests.exceptions.RequestException as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"API request failed: {str(e)}"
            vehicle_data.save()

            return {
                "status_code": 500,
                "response_data": f"API request failed: {str(e)}"
            }
        except ValueError as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            vehicle_data.save()

            return {
                "status_code": 500,
                "response_data": f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            }

    except Exception as e:
        return {
            "status_code": 500,
            "response_data": f"Error: {str(e)}"
        }


# return render(request, 'PITBApi/VTCSTripList.html')


@login_required(login_url='LoginView')
def PushVTCSTripData_FormView(request):
    template_name = "PITBApi/PushVTCSTripData_Form.html"
    vehicles_data_list = VehicleData.objects.filter(pitb_code__isnull=False,
                                                    vehicle_type="Dumper 10m3").only(
        'vehicle_code',
        'pitb_code',
        'register_no').order_by(
        'register_no')

    form = VTCSForm()
    # Initialize empty form for GET requests
    if request.method == "GET":
        form = VTCSForm()
    elif request.method == "POST":
        form = VTCSForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Get GPRS data if available
                gprs = None
                try:
                    gprs_obj = TrackerRawData.objects.filter(
                        gprs_raw_code__isnull=False
                    ).order_by('-id').values_list('gprs_raw_code', flat=True).first()
                    if gprs_obj:
                        gprs = gprs_obj
                except TrackerRawData.DoesNotExist:
                    pass

                # Create but don't save the trip object yet
                trip = form.save(commit=False)
                trip.gprs_raw_code_id = gprs
                trip.save()

                messages.success(request, "Trip data saved successfully.")

                # Determine which button was clicked using the 'action' parameter
                action = request.POST.get("action", "save")
                if action == "push":
                    # Get the ID of the newly created trip and send to PITB API
                    trip_id = trip.id
                    api_response = PostVTCSToPITBAPIById(trip_id)
                    if api_response["status_code"] in [200, 201]:
                        messages.success(request, f"Pushed to PITB system")
                    elif api_response.get("already_sent", False):
                        messages.info(request, "Trip data was already sent to PITB API.")
                    else:
                        messages.warning(request,
                                         f"Trip data saved but failed to push to PITB server: {api_response['response_data']}")
                else:
                    # This is for the "Save in System" button (action="save")
                    messages.info(request, "Trip data saved locally only.")

                # Redirect to same page with a fresh form after successful submission
                return redirect("PushVTCSTripData_Form")

            except Exception as e:
                messages.error(request, f"Error saving trip: {str(e)}")
        else:
            # If form is invalid, show validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    # dumping_site_list = DumpingSite.objects.filter(code="DS-1")
    dumping_site = get_object_or_404(DumpingSite, code="DS-1")
    code_number = dumping_site.code.split('-')[1] if '-' in dumping_site.code else dumping_site.code
    latitude = dumping_site.geom.y if dumping_site.geom else None
    longitude = dumping_site.geom.x if dumping_site.geom else None

    context = {
        'form': form,
        'vehicles_data_list': vehicles_data_list,
        'dumping_site_list': dumping_site,
        'code_number': code_number,
        'latitude': latitude,
        'longitude': longitude,
    }
    return render(request, template_name, context)


def PostVTCSToPITBAPIById(VTCS_id):
    try:
        # Find trips for this vehicle on this date
        vehicle_data = APITripData.objects.filter(
            id=VTCS_id
        ).first()
        print(f"Processing trip ID: {VTCS_id}, Found data: {vehicle_data is not None}")
        if not vehicle_data:
            return {
                "status_code": 404,
                "response_data": f"No trip data found for vehicle {VTCS_id}"
            }
        if vehicle_data.response_status == "Success":
            return {
                "status_code": 200,
                "response_data": f"Data for vehicle {VTCS_id} was already successfully sent to PITB",
                "already_sent": True
            }

        veh_reg_with_pitb = vehicle_data.vehicle_code.pitb_code
        # Prepare the base data without image fields
        extracted_data = {
            "vehicle_no": str(veh_reg_with_pitb),
            "before_weight": float(vehicle_data.before_weight),
            "after_weight": float(vehicle_data.after_weight),
            "time_in": vehicle_data.time_in.strftime('%Y-%m-%d %H:%M:%S'),
            "time_out": vehicle_data.time_out.strftime('%Y-%m-%d %H:%M:%S'),
            "slip_id": str(vehicle_data.slip_id),
            "lat": float(vehicle_data.lat),
            "long": float(vehicle_data.long),
            "site_name": str(vehicle_data.site_name),
            "site_id": str(vehicle_data.site_id),
            "data_id": int(vehicle_data.data_id) if vehicle_data.data_id is not None else None,
        }

        # Prepare files for multipart upload - these are required fields
        files = {}

        # Handle required image fields
        if vehicle_data.before_picture:
            files['before_picture'] = (
                vehicle_data.before_picture.name,
                vehicle_data.before_picture.file,
                'image/jpeg'  # Adjust content type based on actual file type
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required before_picture"
            }

        if vehicle_data.after_picture:
            files['after_picture'] = (
                vehicle_data.after_picture.name,
                vehicle_data.after_picture.file,
                'image/jpeg'  # Adjust content type based on actual file type
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required after_picture"
            }

        # Handle optional image fields
        if vehicle_data.roof_before_picture:
            files['roof_before_picture'] = (
                vehicle_data.roof_before_picture.name,
                vehicle_data.roof_before_picture.file,
                'image/jpeg'
            )

        if vehicle_data.roof_after_picture:
            files['roof_after_picture'] = (
                vehicle_data.roof_after_picture.name,
                vehicle_data.roof_after_picture.file,
                'image/jpeg'
            )

        api_url = "https://elgcd-ms.punjab.gov.pk/api/vtcs/post-trip-data"

        headers = {
            'accept': 'application/json',
            'authkey': 'SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1',
            # 'Content-Type': 'multipart/form-data'
        }

        try:
            response = requests.post(
                url=api_url,
                headers=headers,
                data=extracted_data,
                files=files,  # This will handle the multipart/form-data format correctly
                timeout=30
            )

            # Handle response
            response_data = None
            try:
                response_data = response.json() if response.status_code in [200, 201] else response.text
            except ValueError:
                response_data = response.text

            # Update the APITripData record with the response information
            if response.status_code in [200, 201]:
                # Check if we have json data
                if isinstance(response_data, dict):
                    # Extract data_id from response if available
                    data_id = response_data.get('data_id')
                    message = response_data.get('message', '')
                    # Debug before update
                    print(f"Before update: status={vehicle_data.response_status}, id={vehicle_data.response_id}")

                    # Update record fields
                    vehicle_data.response_id = data_id
                    vehicle_data.response_status = "Success"
                    vehicle_data.remarks = message
                    # Debug after field assignment but before save
                    print(f"Assigned values: id={data_id}, status=Success, remarks={message}")
                    vehicle_data.save()
                    # Debug after save
                    print(f"After save: status={vehicle_data.response_status}, id={vehicle_data.response_id}")
                else:
                    # Handle error case
                    vehicle_data.response_status = "Rejected"
                    vehicle_data.remarks = str(response_data)
                    vehicle_data.save()
            # First Checking if the trip data is already in ApiTripDataLogs
            trip_data_logs = ApiTripDataLogs.objects.filter(trip_data_id=vehicle_data.id).first()
            # if exists then update the trip data logs
            if trip_data_logs:
                trip_data_logs.hit_count += 1
                trip_data_logs.current_response = response_data
                trip_data_logs.save()
            else:
                # Also Adding data in VTCS ApiTripDataLogs

                ApiTripDataLogs.objects.create(
                    trip_data_id=vehicle_data,
                    current_response=response_data,
                    hit_count=1,
                )
            return {
                "status_code": response.status_code,
                "response_data": response_data,
            }
        except requests.exceptions.RequestException as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"API request failed: {str(e)}"
            vehicle_data.save()

            return {
                "status_code": 500,
                "response_data": f"API request failed: {str(e)}"
            }
        except ValueError as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            vehicle_data.save()

            return {
                "status_code": 500,
                "response_data": f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            }

    except Exception as e:
        return {
            "status_code": 500,
            "response_data": f"Error: {str(e)}"
        }


# For updating Trip Data in PITB using response_id
def UpdateVTCSPITBAPIByDataId(response_id):
    try:
        # Find trip using response_id
        vehicle_data = APITripData.objects.filter(
            response_id=response_id
        ).first()
        print(f"Processing trip with response ID: {response_id}, Found data: {vehicle_data is not None}")

        if not vehicle_data:
            return {
                "status_code": 404,
                "response_data": f"No trip data found with response ID {response_id}"
            }

        # Prepare the base data without image fields
        extracted_data = {
            "vehicle_no": str(vehicle_data.vehicle_code.pitb_code),
            "before_weight": float(vehicle_data.before_weight),
            "after_weight": float(vehicle_data.after_weight),
            "time_in": vehicle_data.time_in.strftime('%Y-%m-%d %H:%M:%S'),
            "time_out": vehicle_data.time_out.strftime('%Y-%m-%d %H:%M:%S'),
            "slip_id": str(vehicle_data.slip_id),
            "lat": float(vehicle_data.lat),
            "long": float(vehicle_data.long),
            "site_name": str(vehicle_data.site_name),
            "site_id": str(vehicle_data.site_id),
            "data_id": int(response_id)
        }

        # Prepare files for multipart upload - these are required fields
        files = {}

        # Handle required image fields
        if vehicle_data.before_picture:
            files['before_picture'] = (
                vehicle_data.before_picture.name,
                vehicle_data.before_picture.file,
                'image/jpeg'  # Adjust content type based on actual file type
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required before_picture"
            }

        if vehicle_data.after_picture:
            files['after_picture'] = (
                vehicle_data.after_picture.name,
                vehicle_data.after_picture.file,
                'image/jpeg'
            )
        else:
            return {
                "status_code": 400,
                "response_data": "Missing required after_picture"
            }

        # Handle optional image fields
        if vehicle_data.roof_before_picture:
            files['roof_before_picture'] = (
                vehicle_data.roof_before_picture.name,
                vehicle_data.roof_before_picture.file,
                'image/jpeg'
            )

        if vehicle_data.roof_after_picture:
            files['roof_after_picture'] = (
                vehicle_data.roof_after_picture.name,
                vehicle_data.roof_after_picture.file,
                'image/jpeg'
            )

        api_url = "https://elgcd-ms.punjab.gov.pk/api/vtcs/post-trip-data"

        headers = {
            'accept': 'application/json',
            'authkey': 'SGWMC-SaSg-MC4yMTUxODE0Nzk0MzA5MjY0NzAuMzM3Nzk4MzQ0Mjg1',
            # 'Content-Type': 'multipart/form-data'
        }

        try:
            response = requests.post(
                url=api_url,
                headers=headers,
                data=extracted_data,
                files=files,  # This will handle the multipart/form-data format correctly
                timeout=30
            )

            # Handle response
            response_data = None
            try:
                response_data = response.json() if response.status_code in [200, 201] else response.text
            except ValueError:
                response_data = response.text

            # Update the APITripData record with the response information
            if response.status_code in [200, 201]:
                # Check if we have json data
                if isinstance(response_data, dict):
                    # Extract data_id from response if available
                    data_id = response_data.get('data_id')
                    message = response_data.get('message', '')

                    # Update record fields
                    vehicle_data.remarks = message
                    vehicle_data.save()

                    print(f"Update successful: id={response_id}, remarks={message}")
                else:
                    # Handle error case
                    vehicle_data.response_status = "Rejected"
                    vehicle_data.remarks = str(response_data)
                    vehicle_data.save()

            return {
                "status_code": response.status_code,
                "response_data": response_data,
            }
        except requests.exceptions.RequestException as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"API request failed: {str(e)}"
            vehicle_data.save()

            # Here we are updating the ApiTripDataLogs of that vehicle
            trip_data = APITripData.objects.filter(response_id=response_id).first()
            trip_data_log = ApiTripDataLogs.objects.filter(trip_data_id=trip_data).first()
            if trip_data_log:
                trip_data_log.hit_count += 1
                trip_data_log.current_response = response_data
                trip_data_log.save()
            else:
                ApiTripDataLogs.objects.create(
                    trip_data_id=trip_data,
                    current_response=response_data,
                    hit_count=1,
                )

            return {
                "status_code": 500,
                "response_data": f"API request failed: {str(e)}"
            }
        except ValueError as e:
            # Update record with error information
            vehicle_data.response_status = "Rejected"
            vehicle_data.remarks = f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            vehicle_data.save()

            return {
                "status_code": 500,
                "response_data": f"Failed to parse API response: {str(e)}, Response text: {response.text}"
            }

    except Exception as e:
        return {
            "status_code": 500,
            "response_data": f"Error: {str(e)}"
        }
