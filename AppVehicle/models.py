import uuid

from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models

from AppRoute.models import *


# Create your models here.

# Owner Data Model
class OwnerData(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Block', 'Block'),
    ]
    OWNER_TYPE_CHOICES = [
        ('Self', 'Self'),
        ('Vendor', 'Vendor')
    ]
    id = models.AutoField(primary_key=True)
    owner_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200, null=True)
    cnic = models.CharField(max_length=15, null=True, unique=True)  # CNIC of Owner
    address = models.TextField(max_length=500, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    owner_type = models.CharField(max_length=10, choices=OWNER_TYPE_CHOICES, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_owner_data'

    def __str__(self):
        return self.owner_code


class VehicleType(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_type_code = models.CharField(max_length=200, null=True, unique=True)
    vehicle_type_name = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    description = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)
    vehicle_icon = models.ImageField(upload_to='VehicleIcon/', null=True)

    class Meta:
        db_table = 'tbl_vehicle_type'

    def __str__(self):
        return self.vehicle_type_name


class VehicleUsedFor(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_use_code = models.CharField(max_length=200, null=True, unique=True)
    vehicle_use_name = models.TextField(max_length=100, null=True)
    description = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_use_for'

    def __str__(self):
        return self.vehicle_use_name


class VehicleData(models.Model):
    OWNERSHIP_STATUS = [
        ('Owner', 'Owner'),
        ('Rented', 'Rented'),
    ]
    VTMS_STATUS_CHOICES = [
        ('Working', 'Working'),
        ('Stop', 'Stop')
    ]
    id = models.AutoField(primary_key=True)
    vehicle_code = models.CharField(max_length=200, null=True,
                                    unique=True)  # GIS and USTI Code Save in Same Column (VehicleId)
    vendor_code = models.TextField(max_length=100, null=True)  # VENDOR GPRS SOFTWARE SYSTEM CODE (VehID)
    register_no = models.TextField(max_length=200, null=True)
    make = models.TextField(max_length=200, null=True)
    engine_no = models.TextField(max_length=200, null=True)
    chasis_no = models.TextField(max_length=200, null=True)
    color = models.TextField(max_length=200, null=True)
    model = models.TextField(max_length=200, null=True)
    cc = models.TextField(max_length=200, null=True)
    fuel_type = models.TextField(max_length=200, null=True)
    total_mileage = models.FloatField(null=True)
    vehicle_type = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    pitb_code = models.TextField(max_length=100, null=True)  # PITB CODE (VehID)
    mileage_cur_value = models.FloatField(null=True, blank=True)
    date_installed = models.DateField(null=True, blank=True)
    installation_date = models.DateTimeField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    engin_temp = models.FloatField(null=True, blank=True)
    engine_hours = models.FloatField(null=True, blank=True)
    fuel_level = models.FloatField(null=True, blank=True)
    fuel_consumed = models.FloatField(null=True, blank=True)
    ext_bat_voltage = models.FloatField(null=True, blank=True)
    int_bat_voltage = models.FloatField(null=True, blank=True)
    veh_status_chg_sec = models.IntegerField(null=True, blank=True)
    owner = models.ForeignKey(OwnerData, to_field='owner_code', on_delete=models.CASCADE, null=True)
    ownership_status = models.CharField(max_length=10, choices=OWNERSHIP_STATUS, default='Owner')
    vtms_status = models.CharField(max_length=12, choices=VTMS_STATUS_CHOICES, default='Working')
    vehicle_use_code = models.ForeignKey(VehicleUsedFor, to_field='vehicle_use_code', on_delete=models.CASCADE,
                                         null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_data'

    def __str__(self):
        return self.register_no


class VehicleDataLog(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    before_data = models.JSONField(null=True)
    after_data = models.JSONField(null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_data_logs'


class DriverData(models.Model):
    id = models.AutoField(primary_key=True)
    driver_code = models.CharField(max_length=200, null=True, unique=True)  # GIS and USTI Code Save in Same Column
    name = models.TextField(max_length=100, null=True)
    cnic = models.CharField(max_length=15, null=True, unique=True)
    license_no = models.CharField(max_length=25, null=True, unique=True)
    license_expiry = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_driver_data'

    def __str__(self):
        return self.driver_code


class VehicleDriver(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    driver_code = models.ForeignKey(DriverData, to_field='driver_code', on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_driver'

        def __str__(self):
            return f'{self.vehicle_code}-{self.driver_code}'


# EQUIPMENT DETAILS


class TrackerVehicle(models.Model):
    id = models.AutoField(primary_key=True)
    terminal_no = models.CharField(max_length=200, null=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    company_name = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active, Block
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_tracker_vehicle'

    def __str__(self):
        return self.vehicle_code


class TrackerRawData(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    gprs_raw_code = models.CharField(max_length=200, null=True, unique=True)
    terminal_no = models.BigIntegerField(null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    rms_error = models.TextField(max_length=200, null=True)
    g_status = models.TextField(max_length=200, null=True)  # Parked
    vehicle_status = models.TextField(max_length=200, null=True)  # Moving
    device_status = models.TextField(max_length=200, null=True)  # ACC On,Moving
    vendor_date_time = models.DateTimeField(blank=True)
    system_date_time = models.DateTimeField(blank=True)
    speed = models.FloatField(null=True)
    avg_speed = models.FloatField(null=True)
    max_speed = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    direction = models.IntegerField(null=True)
    mileage = models.IntegerField(null=True)
    push_status = models.TextField(max_length=200, null=True)  # Pending/Completed
    sync_code = models.TextField(max_length=200, null=True)  # Pending/Completed
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    location = models.TextField(max_length=500, null=True, blank=True)
    location_a = models.TextField(max_length=500, null=True, blank=True)
    gis_geo_status = models.CharField(max_length=50, null=True, blank=True)
    mileage_cur_value = models.FloatField(null=True, blank=True)
    acc_status = models.CharField(max_length=50, null=True, blank=True)  # On/Off
    rpm = models.FloatField(null=True, blank=True)
    engine_temp = models.FloatField(null=True, blank=True)
    engine_hours = models.FloatField(null=True, blank=True)
    fuel_level = models.FloatField(null=True, blank=True)
    fuel_consumed = models.FloatField(null=True, blank=True)
    gps_satelite = models.IntegerField(null=True, blank=True)
    gsm_signal = models.FloatField(null=True, blank=True)
    ext_bat_voltage = models.FloatField(null=True, blank=True)
    int_bat_voltage = models.FloatField(null=True, blank=True)
    # working_hours = models.FloatField(null=True, blank=True, default=0.0)
    threshold_status = models.CharField(max_length=50, null=True, blank=Tru
    working_hours = models.DecimalField(null=True, blank=True, default=Decimal("0.00"), max_digits=10, decimal_places=2)e)  # Yes/No
    minutes_diff = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)  # For manual verification of data
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_tracker_raw_data'

    def __str__(self):
        return self.vehicle_code


class VehicleLiveMonitor(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True,
                                     related_name='live_monitor')
    veh_live_mont_code = models.CharField(max_length=200, null=True, unique=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    rms_error = models.TextField(max_length=200, null=True)
    g_status = models.TextField(max_length=200, null=True)  # Parked
    speed = models.FloatField(null=True)
    direction = models.IntegerField(null=True)
    device_status = models.TextField(max_length=200, null=True)  # ACC On,Moving
    ignition_status = models.TextField(max_length=200, null=True)  # ACC On,Moving
    geo_location = models.TextField(max_length=200, null=True)  # ACC On,Moving
    vendor_date_time = models.TextField(max_length=200, null=True)
    duration = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)
    gsm_signal = models.FloatField(null=True, blank=True)
    ext_bat_voltage = models.FloatField(null=True, blank=True)
    int_bat_voltage = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_vehicle_live_monitor'

    def __str__(self):
        return self.vehicle_code


class TrackerSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    check_in = models.DateTimeField(blank=True)
    check_out = models.DateTimeField(blank=True)
    time_duration = models.TextField(max_length=200, null=True)
    process_status = models.TextField(max_length=200, null=True)  # Pending/Completed
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_tracker_schedule'

    def __str__(self):
        return self.created_at


class WorkScheduleGPRSApi(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # WS-1
    work_date = models.DateField(blank=True)
    run_count = models.TextField(max_length=200, null=True)
    process_status = models.TextField(max_length=200, null=True)  # Pending, Completed
    description = models.TextField(max_length=200,
                                   null=True)  # IF BACKUP DATA SYNC THEN (Sync-Finished), For Current Date (Sync-Current)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_work_schedule_gprs_api'

    def __str__(self):
        return self.created_at


class VehicleScheduleGPRSApi(models.Model):
    IGNITION_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    THRESHOLD_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    id = models.AutoField(primary_key=True)
    veh_api_code = models.CharField(max_length=200, null=True, unique=True)  # VAI-1
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    wsa_code = models.ForeignKey(WorkScheduleGPRSApi, to_field='code', on_delete=models.CASCADE, null=True)
    process_done = models.DateTimeField(blank=True, null=True)
    retrieve_record = models.IntegerField(null=True)
    vendor_record = models.IntegerField(null=True)
    process_status = models.TextField(max_length=200, null=True)  # Pending, Completed
    veh_sch_date = models.DateField(blank=True)
    ignition_status = models.CharField(max_length=3, choices=IGNITION_CHOICES, null=True, default='No')
    distance = models.FloatField(null=True, default=0.0)
    working_hours = models.FloatField(null=True, default=0.0)
    threshold = models.CharField(max_length=3, choices=THRESHOLD_CHOICES, null=True, default='No')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_schedule_gprs_api'

    def __str__(self):
        return self.vehicle_code


class ContainerTrackerGPRS(models.Model):
    id = models.AutoField(primary_key=True)
    gprs_raw_code = models.ForeignKey(TrackerRawData, to_field='gprs_raw_code', on_delete=models.CASCADE, null=True)
    container_code = models.ForeignKey(ContainerData, to_field='container_code', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_container_tracker_gprs'

    def __str__(self):
        return self.container_code


class VehicleTripData(models.Model):
    id = models.AutoField(primary_key=True)
    vtd_code = models.CharField(max_length=200, null=True, unique=True)  # VTD-1
    trip_code = models.CharField(max_length=200, null=True)  # TRIP-1
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    from_check_in = models.DateTimeField(blank=True, null=True)
    from_check_out = models.DateTimeField(blank=True, null=True)
    from_time_spent = models.TextField(max_length=200, null=True)
    from_side = models.TextField(max_length=200, null=True)
    to_side = models.TextField(max_length=200, null=True)
    to_check_in = models.DateTimeField(blank=True, null=True)
    to_check_out = models.DateTimeField(blank=True, null=True)
    to_time_spent = models.TextField(max_length=200, null=True)
    parent_code = models.TextField(max_length=200, null=True)
    description = models.TextField(null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_trip_data'

    def __str__(self):
        return self.vtd_code


class VehicleTripGPRSData(models.Model):
    id = models.AutoField(primary_key=True)
    vtgd_code = models.CharField(max_length=200, null=True, unique=True)  # VTGD-1
    vtd_code = models.ForeignKey(VehicleTripData, to_field='vtd_code', on_delete=models.CASCADE, null=True)
    gprs_raw_code = models.ForeignKey(TrackerRawData, to_field='gprs_raw_code', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_trip_gprs_data'

    def __str__(self):
        return self.vtgd_code


# DELETED
class WeighingTripData(models.Model):
    id = models.AutoField(primary_key=True)
    wgt_code = models.CharField(max_length=200, null=True, unique=True)  # WGT-1
    vtd_code = models.ForeignKey(VehicleTripData, to_field='vtd_code', on_delete=models.CASCADE, null=True)
    total_weight = models.FloatField(null=True)
    reference_no = models.FloatField(null=True)
    attachment = models.ImageField(upload_to='Invoice/WeighingBill', null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_weighing_trip_data'

    def __str__(self):
        return self.wgt_code


class VehicleDependentApi(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # WGT-1
    vehicle_type_code = models.ForeignKey(VehicleType, to_field='vehicle_type_code', on_delete=models.CASCADE,
                                          null=True)
    pitb_api_code = models.TextField(max_length=200, null=True)
    description = models.TextField(null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_vehicle_dependent_api'

    def __str__(self):
        return self.vehicle_type_code


PENDING = 'Pending'
COMPLETED = 'Completed'

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (COMPLETED, 'Completed'),
]


# Complaint System Models
class Complaint(models.Model):
    # PENDING='Pending'
    # COMPLETED='Completed'
    #
    # STATUS_CHOICES=[
    #     (PENDING, 'Pending'),
    #     (COMPLETED, 'Completed'),
    # ]

    complaint_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True)
    remarks = models.TextField(null=True, blank=True)  # Only be filled by the complaint Handler

    class Meta:
        db_table = 'tbl_complaint'

    def _str_(self):
        return str(self.complaint_code)


# 7/4/2025
class VehicleThreshold(models.Model):
    IGNITION_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    id = models.AutoField(primary_key=True)
    vehicle_type = models.CharField(max_length=100, null=True)
    distance = models.FloatField(null=True, default=0)
    min_distance = models.FloatField(null=True, default=0)
    working_hours = models.FloatField(null=True)
    ignition_status = models.CharField(max_length=3, choices=IGNITION_CHOICES, null=True, default='No')
    description = models.TextField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, default="admin")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=200, null=True, default="admin")

    class Meta:
        db_table = 'tbl_vehicle_threshold'


class TrackerCompany(models.Model):
    id = models.AutoField(primary_key=True)
    company_code = models.CharField(max_length=200, null=True, unique=True)  # 01
    company_name = models.CharField(max_length=100, null=True)  # Mardo Group
    uan_no = models.CharField(max_length=200, null=True)
    ntn_no = models.CharField(max_length=200, null=True)
    strn_no = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    area = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_company'

    def __str__(self):
        return self.company_name


class TrackerData(models.Model):
    TERMINAL_TYPES = [
        ('installed', 'Installed'),
        ('advanced', 'Advanced'),
    ]

    terminal_code = models.CharField(max_length=100, unique=True)
    # tracker_company_code = models.ForeignKey(TrackerCompany, to_field='company_code', on_delete=models.CASCADE)
    tracker_company_code = models.CharField(max_length=100)
    modal_no = models.CharField(max_length=100, null=True, blank=True)
    minutes_diff = models.IntegerField(null=True, blank=True)
    ins_co = models.CharField(max_length=100, null=True, blank=True)  # Insurance Company
    region = models.CharField(max_length=50, null=True, blank=True)
    group_title = models.CharField(max_length=100, null=True, blank=True)
    gps_satelite = models.IntegerField(null=True, blank=True)
    gsm_signal = models.FloatField(null=True, blank=True)
    sale_type_name = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Insurance With Tracker"
    # status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Blocked', 'Blocked')], default='Active')
    terminal_type = models.CharField(max_length=10, choices=TERMINAL_TYPES)
    reason = models.TextField(null=True, blank=True)  # Reason for block or replacement
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True, default="admin")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_tracker_data'

    def __str__(self):
        return self.terminal_code


class TrackerDataLog(models.Model):
    start_time = models.DateTimeField()  # When old terminal was assigned
    end_time = models.DateTimeField(auto_now_add=True)  # When new terminal was assigned
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_tracker_data_log'


class TrackerVehicleData(models.Model):
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    terminal_code = models.ForeignKey(TrackerData, to_field='terminal_code', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Blocked', 'Blocked')], default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.terminal_code

    class Meta:
        db_table = 'tbl_tracker_vehicle_data'


class TrackerVehicleLog(models.Model):
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE)
    old_terminal_code = models.CharField(max_length=100)
    new_terminal_code = models.CharField(max_length=100)
    start_time = models.DateTimeField()  # When old terminal was assigned
    end_time = models.DateTimeField(auto_now_add=True)  # When new terminal was assigned
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_tracker_vehicle_log'

    def __str__(self):
        return f"{self.vehicle_code} changed from {self.old_terminal_code} to {self.new_terminal_code}"


class TelecomData(models.Model):
    telecom_id = models.AutoField(primary_key=True)
    sim_no = models.CharField(max_length=50, unique=True)
    gsm_co = models.CharField(max_length=100)
    connected = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_telecom_data'

    def __str__(self):
        return self.sim_no


class TrackerTelecomData(models.Model):
    terminal = models.ForeignKey(TrackerVehicleData, on_delete=models.CASCADE, related_name='tracker_telecom_data')
    sim = models.ForeignKey(TelecomData, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Active')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.CharField(max_length=100, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_tracker_telecom_data'

    def __str__(self):
        return f'{self.terminal.terminal_code} - {self.sim.sim_no}'


class Customer(models.Model):
    customer_no = models.CharField(max_length=50, null=True, blank=True, unique=True)
    customer_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    str_dob = models.CharField(max_length=50, null=True, blank=True)
    cnic_no = models.CharField(max_length=20, null=True, blank=True)
    cell_phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_ph1 = models.CharField(max_length=20, null=True, blank=True)
    emergency_cel1 = models.CharField(max_length=20, null=True, blank=True)
    ins_co = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    group_title = models.CharField(max_length=100, null=True, blank=True)
    ins_br = models.CharField(max_length=100, null=True, blank=True)
    ins_agn = models.CharField(max_length=100, null=True, blank=True)
    ins_sd = models.DateTimeField(null=True, blank=True)  # Insurance Start Date
    ins_ed = models.DateTimeField(null=True, blank=True)  # Insurance End Date
    str_ins_sd = models.CharField(max_length=50, null=True, blank=True)
    str_ins_ed = models.CharField(max_length=50, null=True, blank=True)
    sale_type_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, default="admin")
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True, default="admin")

    class Meta:
        db_table = 'tbl_customer_data'

    def __str__(self):
        return self.name


class VehicleTerminalPairing(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicle_pairings')
    vehicle_code = models.ForeignKey(VehicleData, to_field='vehicle_code', on_delete=models.CASCADE, null=True)
    old_terminal = models.ForeignKey(TrackerData, on_delete=models.CASCADE, null=True, to_field='terminal_code',
                                     related_name='old_terminal')
    new_terminal = models.ForeignKey(TrackerData, on_delete=models.CASCADE, null=True, to_field='terminal_code',
                                     related_name='new_terminal')
    installation_date = models.DateField(auto_now_add=True)
    testing_time_from = models.TimeField(null=True, blank=True)
    testing_time_to = models.TimeField(null=True, blank=True)
    meter_reading = models.FloatField(null=True)
    install_type = models.CharField(max_length=150, null=True)
    location = models.CharField(max_length=200, null=True)
    remarks = models.TextField(null=True)
    region = models.CharField(max_length=200, null=True)
    technician_name = models.CharField(max_length=150, null=True)
    installation_place = models.CharField(max_length=200, null=True)

    old_customer_number = models.CharField(max_length=50, null=True, blank=True)
    old_vehicle_pitb_code = models.CharField(max_length=50, null=True, blank=True)
    old_vehicle_register_no = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True, default="admin")

    class Meta:
        db_table = 'tbl_vehicle_terminal_pairing'
