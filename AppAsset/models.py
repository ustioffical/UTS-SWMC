from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models

from AppSetting.models import *


# Create your models here.
class AssetGroup(models.Model):
    id = models.AutoField(primary_key=True)
    asset_group_code = models.CharField(max_length=200, null=True, unique=True)  # AG-1
    asset_group_name = models.TextField(max_length=100, null=True)
    description = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_asset_group'

    def __str__(self):
        return self.asset_group_name


class AssetType(models.Model):
    id = models.AutoField(primary_key=True)
    asset_code = models.CharField(max_length=100, null=True, unique=True)  # AT-1
    asset_name = models.TextField(max_length=100, null=True)
    asset_group_code = models.ForeignKey(AssetGroup, to_field='asset_group_code', on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    model_table = models.TextField(max_length=200, null=True)  # tbl_disposal
    shape_type = models.TextField(max_length=100, null=True)  # Point, Line, Polygon
    manual_code = models.TextField(max_length=100, null=True)
    image = models.ImageField(upload_to='AssetType', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_asset_type'

    def __str__(self):
        return self.asset_name


class AssetGeoFence(models.Model):
    id = models.AutoField(primary_key=True)
    geofence_code = models.CharField(max_length=100, null=True, unique=True)  # GF-1
    asset_code = models.ForeignKey(AssetType, to_field='asset_code', on_delete=models.CASCADE, null=True)
    distance = models.IntegerField(null=True)  # Approve
    radius = models.IntegerField(null=True)  # Approve
    description = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    model_table = models.TextField(max_length=200, null=True)  # tbl_container_data
    shape_type = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # POLYGON
    feature_code = models.TextField(max_length=100, null=True)  # NEW FROM AMIS
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_asset_geo_fence'

    def __str__(self):
        return self.geofence_code


class CollectionSite(models.Model):
    id = models.AutoField(primary_key=True)
    tcp_code = models.CharField(max_length=200, null=True, unique=True)  # TCP-1
    tcp_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    admin_code = models.ForeignKey(AdministrativeBoundary, to_field='admin_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/TCP', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_collection_site'

    def __str__(self):
        return self.tcp_name


class WeighingSite(models.Model):
    id = models.AutoField(primary_key=True)
    weigh_code = models.CharField(max_length=200, null=True, unique=True)  # WGS-1
    weigh_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/WeighingSite', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_weighing_site'

    def __str__(self):
        return self.weigh_name


class WeighingCoverage(models.Model):
    id = models.AutoField(primary_key=True)
    weigh_code = models.ForeignKey(WeighingSite, to_field='weigh_code', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # WGC-1
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Polygon
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_weighing_coverage'

    def __str__(self):
        return self.weigh_code


class DumpingSite(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # DS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/DumpingSite', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_dumping_site'

    def __str__(self):
        return self.name


class DumpingCoverage(models.Model):
    id = models.AutoField(primary_key=True)
    dump_site_code = models.ForeignKey(DumpingSite, to_field='code', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # DC-1
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Polygon
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_dumping_coverage'

    def __str__(self):
        return self.dump_site_code


class ParkingSite(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # PS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/ParkingSite', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_parking_site'

    def __str__(self):
        return self.name


class Workshop(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # WS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/ParkingSite', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_workshop'

    def __str__(self):
        return self.name


class TransferStation(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # TS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/TransferStation', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_transfer_station'

    def __str__(self):
        return self.name


class FillingStation(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # TS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/FillingStation', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_filling_station'

    def __str__(self):
        return self.name


class LandfillSite(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200, null=True, unique=True)  # TS-1
    name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)  # Point
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/Landfill', null=True)
    install_year = models.DateField(null=True)  # Date
    condition = models.TextField(max_length=200, null=True)  # GOOD, EXCELLENT, FAIR, POOR, FAILURE
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_landfill_site'

    def __str__(self):
        return self.name


class ContainerType(models.Model):
    id = models.AutoField(primary_key=True)
    container_type_code = models.CharField(max_length=200, null=True, unique=True)
    container_type_name = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_container_type'

    def __str__(self):
        return self.container_type_name


class ContainerData(models.Model):
    id = models.AutoField(primary_key=True)
    system_code = models.TextField(max_length=100, null=True)  # NEW FROM AMIS
    container_code = models.CharField(max_length=200, null=True, unique=True)  # CNT-1
    container_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    admin_code = models.ForeignKey(AdministrativeBoundary, to_field='admin_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/Container', null=True)
    size = models.TextField(max_length=200, null=True)
    install_year = models.DateField(null=True)  # Date
    asset_condition = models.TextField(max_length=200, null=True)
    category = models.TextField(max_length=200, null=True)
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional     # Approve
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    repeat_id = models.IntegerField(null=True)
    repeat_geom = models.IntegerField(null=True)
    serial_geom = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_container_data'

    def __str__(self):
        return self.container_name


class ContainerProcessType(models.Model):
    id = models.AutoField(primary_key=True)
    cont_proc_type_code = models.CharField(max_length=200, null=True, unique=True)  # CPT-1
    cont_proc_type_name = models.TextField(max_length=100, null=True)  # Approve
    duration_mint = models.TextField(max_length=200, null=True)
    description = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_container_process_type'

    def __str__(self):
        return self.cont_proc_type_name


class ContainerProcess(models.Model):
    id = models.AutoField(primary_key=True)
    container_code = models.ForeignKey(ContainerData, to_field='container_code', on_delete=models.CASCADE, null=True)
    cont_proc_type_code = models.ForeignKey(ContainerProcessType, to_field='cont_proc_type_code',
                                            on_delete=models.CASCADE, null=True)
    container_process_code = models.CharField(max_length=200, null=True, unique=True)  # CP-1
    check_in = models.TextField(max_length=200, null=True)
    check_out = models.TextField(max_length=200, null=True)
    net_time_spent = models.TextField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    vehicle_code_id = models.TextField(max_length=200, null=True)  # VEHICLE CODE TEXT
    created_at = models.DateTimeField(null=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_container_process'

    def __str__(self):
        return self.container_code


class DrumData(models.Model):
    id = models.AutoField(primary_key=True)
    drum_code = models.CharField(max_length=200, null=True, unique=True)  # DM-1
    drum_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    admin_code = models.ForeignKey(AdministrativeBoundary, to_field='admin_code', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Asset/Container', null=True)
    install_year = models.DateField(null=True)  # Date
    asset_condition = models.TextField(max_length=200, null=True)
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    repeat_id = models.IntegerField(null=True)
    repeat_geom = models.IntegerField(null=True)
    serial_geom = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, auto_now=True)  # Approve
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_drum_data'

    def __str__(self):
        return self.drum_name
