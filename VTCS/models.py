from django.db import models
from AppVehicle.models import VehicleData, TrackerRawData
from DataLogs.models import APITransmissionData
from datetime import datetime
import os


def before_picture_path(instance, filename):
    base, ext = os.path.splitext(filename)
    dt_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_filename = f"{base}{dt_str}{ext}"
    return os.path.join('trip_pics/before/', new_filename)

def after_picture_path(instance, filename):
    base, ext = os.path.splitext(filename)
    dt_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_filename = f"{base}{dt_str}{ext}"
    return os.path.join('trip_pics/after/', new_filename)

def roof_before_picture_path(instance, filename):
    base, ext = os.path.splitext(filename)
    dt_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_filename = f"{base}{dt_str}{ext}"
    return os.path.join('trip_pics/roof_before/', new_filename)

def roof_after_picture_path(instance, filename):
    base, ext = os.path.splitext(filename)
    dt_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    new_filename = f"{base}{dt_str}{ext}"
    return os.path.join('trip_pics/roof_after/', new_filename)

class APITripData(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    gprs_raw_code = models.ForeignKey(TrackerRawData, to_field='gprs_raw_code', on_delete=models.CASCADE, null=True)
    tms_code = models.ForeignKey(APITransmissionData, to_field='tms_code', on_delete=models.CASCADE, null=True)
    trip_date = models.DateField(null=True)

    before_weight = models.FloatField()  # Weight before unloading (kg)
    after_weight = models.FloatField()  # Weight after unloading (kg)
    time_in = models.DateTimeField()  # Entry timestamp
    time_out = models.DateTimeField()  # Exit timestamp
    # VTCS - Trip
    before_picture = models.ImageField(upload_to=before_picture_path)  # Required
    after_picture = models.ImageField(upload_to=after_picture_path)  # Required
    roof_before_picture = models.ImageField(upload_to=roof_before_picture_path, null=True, blank=True)  # Optional
    roof_after_picture = models.ImageField(upload_to=roof_after_picture_path, null=True, blank=True)  # Optional

    uuid = models.CharField(max_length=100, null=True, blank=True)  # Optional unique trip ID
    slip_id = models.IntegerField(unique=True)  # Waste collection slip ID
    data_id = models.IntegerField(null=True, blank=True)  # For update reference

    lat = models.FloatField()  # Latitude of dumping site
    long = models.FloatField()  # Longitude of dumping site

    site_name = models.CharField(max_length=255)  # Name of dumping site
    site_id = models.CharField(max_length=100)  # Landfill site ID
    response_id = models.IntegerField(null=True, blank=True)
    response_status = models.CharField(max_length=100, null=True, blank=True)  # Success,Rejected
    remarks = models.TextField(null=True, blank=True)  # Remarks for the trip
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Trip {self.vehicle_code} at {self.site_name} ({self.time_in})"

    class Meta:
        db_table = 'tbl_api_trip_data'


class ApiTripDataLogs(models.Model):
    id = models.AutoField(primary_key=True)
    trip_data_id = models.ForeignKey(APITripData, related_name='trip_data_logs', on_delete=models.CASCADE)
    current_response = models.TextField(null=True, blank=True)
    hit_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_api_trip_data_logs'
