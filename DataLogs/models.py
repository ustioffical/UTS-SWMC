from django.db import models
from AppVehicle.models import VehicleData,TrackerRawData
from PITB_API_DATA.models import PITBApiData
from django.db.models.signals import pre_save
from django.dispatch import receiver

class APITransmissionData(models.Model):
    ACTIVE = 'active'
    BLOCKED = 'blocked'

    STATUS_CHOICES = [
        (ACTIVE, 'active'),
        (BLOCKED, 'blocked'),
    ]

    COMPLETED = 'completed'
    REJECTED = 'rejected'

    RESPONSE_STATUS = [
        (COMPLETED, 'completed'),
        (REJECTED, 'rejected'),
    ]
    id = models.AutoField(primary_key=True)
    tms_code = models.CharField(max_length=10, unique=True)  # TSM-1
    pitb_api_code = models.ForeignKey(PITBApiData, to_field='code', on_delete=models.CASCADE, null=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    response_code = models.CharField(max_length=100)
    response_status = models.CharField(max_length=10, choices=RESPONSE_STATUS)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)

# Signal to generate tms_code
@receiver(pre_save, sender=APITransmissionData)
def generate_tms_code(sender, instance, **kwargs):
    if not instance.tms_code:
        last_record = APITransmissionData.objects.all().order_by('-tms_code').first()
        if last_record:
            last_number = int(last_record.tms_code.split('-')[1])
            instance.tms_code = f"TMS-{last_number + 1}"
        else:
            instance.tms_code = "TMS-1"
