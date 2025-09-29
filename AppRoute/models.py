from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models

from AppSetting.models import *
from AppAsset.models import *


# Create your models here.


class RouteNetwork(models.Model):
    id = models.AutoField(primary_key=True)
    route_line_code = models.CharField(max_length=200, null=True, unique=True)  # RNL-1
    route_line_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True)  # Approve
    longitude = models.FloatField(null=True)  # Approve
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    type = models.TextField(max_length=200, null=True)
    row_m = models.TextField(max_length=200, null=True)
    length = models.TextField(max_length=200, null=True)
    speed_limit = models.TextField(max_length=200, null=True)
    category = models.TextField(max_length=200, null=True)  # Excellent, Good, Fair, Poor, Failure
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_route_network'

    def __str__(self):
        return self.route_line_name


class RouteNetworkBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    route_line_code = models.ForeignKey(RouteNetwork, to_field='route_line_code', on_delete=models.CASCADE, null=True)
    route_code = models.CharField(max_length=200, null=True, unique=True)  # RNB-1
    route_name = models.TextField(max_length=100, null=True)  # Approve
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    address = models.TextField(max_length=200, null=True)
    area = models.TextField(max_length=100, null=True)
    upload_type = models.TextField(max_length=200, null=True)  # Manual, System, Shpefile, Kml
    row_m = models.TextField(max_length=200, null=True)
    length = models.TextField(max_length=200, null=True)
    speed_limit = models.TextField(max_length=200, null=True)
    category = models.TextField(max_length=200, null=True)  # Grouped, Un-Grouped
    working_status = models.TextField(max_length=200, null=True)  # Functional, Non-Functional
    plan_status = models.TextField(max_length=200, null=True)  # Verified, Proposed, Survey   (Added by us)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_route_network_boundary'

    def __str__(self):
        return self.route_name


class RouteNetworkSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    route_sche_code = models.CharField(max_length=200, null=True, unique=True)  # RSC-1
    sche_group_code = models.TextField(max_length=200, null=True)
    sche_group_name = models.TextField(max_length=200, null=True)
    route_code = models.ForeignKey(RouteNetworkBoundary, to_field='route_code', on_delete=models.CASCADE, null=True)
    mc_code = models.ForeignKey(MCBoundary, to_field='mc_code', on_delete=models.CASCADE, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_route_network_schedule'

    def __str__(self):
        return self.sche_group_name


class RouteContainer(models.Model):
    id = models.AutoField(primary_key=True)
    route_cont_code = models.CharField(max_length=200, null=True, unique=True)  # RCC-1
    container_code = models.ForeignKey(ContainerData, to_field='container_code', on_delete=models.CASCADE, null=True)
    route_sche_code = models.ForeignKey(RouteNetworkSchedule, to_field='route_sche_code', on_delete=models.CASCADE,
                                        null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(null=True, auto_now=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)  # Approve
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_route_container'

    def __str__(self):
        return self.route_cont_code
