from django.db import models
from AppVehicle.models import VehicleData, TrackerRawData
from DataLogs.models import APITransmissionData
from django.db.models.signals import pre_save
from django.dispatch import receiver


class APIVTMSData(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # VTM-1
    gprs_raw_code = models.ForeignKey(TrackerRawData, to_field='gprs_raw_code', on_delete=models.CASCADE, null=True)
    tms_code = models.ForeignKey(APITransmissionData, to_field='tms_code', on_delete=models.CASCADE, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    vehicle_status = models.TextField(null=True, blank=True)
    engine_status = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.vehicle_status} - {self.engine_status}"

    class Meta:
        db_table = 'tbl_api_vtms_data'


@receiver(pre_save, sender=APIVTMSData)
def generate_code(instance, **kwargs):
    if not instance.code:
        last_record = APIVTMSData.objects.all().order_by('-code').first()
        if last_record:
            last_number = int(last_record.code.split('-')[1])
            instance.code = f"VTM-{last_number + 1}"
        else:
            instance.code = "VTM-1"


class APIVTMSStopPointBulk(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code',
                                     on_delete=models.CASCADE, null=True)
    tms_code = models.ForeignKey(APITransmissionData, to_field='tms_code',
                                 on_delete=models.CASCADE, null=True)
    gprs_raw_code = models.ForeignKey(TrackerRawData, to_field='gprs_raw_code',
                                      on_delete=models.CASCADE, null=True)
    stopped_minutes = models.FloatField(null=True, blank=True)
    stopped_time = models.TimeField()
    restart_time = models.TimeField()
    lat = models.FloatField()
    long = models.FloatField()
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_api_vtms_stop_point_bulk'