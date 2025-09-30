from django.db import models
from django.contrib.gis.db import models


# Create your models here.

class DivisionBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    division_code = models.CharField(max_length=200, null=True, unique=True)
    division_name = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    province = models.TextField(max_length=200, null=True)
    province_u = models.TextField(max_length=200, null=True)
    shape_area = models.FloatField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_division_boundary'

    def __str__(self):
        return self.division_name


class DistrictBoundry(models.Model):
    id = models.AutoField(primary_key=True)
    district_code = models.CharField(max_length=200, null=True, unique=True)
    district_name = models.TextField(max_length=100, null=True)
    division_code = models.ForeignKey(DivisionBoundary, to_field='division_code', on_delete=models.CASCADE, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    province = models.TextField(max_length=200, null=True)
    shape_leng = models.FloatField(max_length=200, null=True)
    shape_area = models.FloatField(max_length=200, null=True)
    status = models.TextField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_district_boundry'

    def __str__(self):
        return self.district_name


class TehsilBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    tehsil_code = models.CharField(max_length=200, null=True, unique=True)
    tehsil_name = models.TextField(max_length=100, null=True)
    district_code = models.ForeignKey(DistrictBoundry, to_field='district_code', on_delete=models.CASCADE, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    status = models.TextField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_tehsil_boundary'

    def __str__(self):
        return self.tehsil_name


class LanduseBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    landuse_code = models.CharField(max_length=200, null=True, unique=True)
    landuse_name = models.TextField(max_length=100, null=True)
    tehsil_code = models.ForeignKey(TehsilBoundary, to_field='tehsil_code', on_delete=models.CASCADE, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    status = models.TextField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_landuse_boundary'

    def __str__(self):
        return self.landuse_name


class TownBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    town_code = models.CharField(max_length=200, null=True, unique=True)
    town_name = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    province = models.TextField(max_length=200, null=True)
    shape_area = models.FloatField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_town_boundary'

    def __str__(self):
        return self.town_name


class ZoneBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    town_code = models.ForeignKey(TownBoundary, to_field='town_code', on_delete=models.CASCADE, null=True)
    zone_code = models.CharField(max_length=200, null=True, unique=True)
    zone_name = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    shape_area = models.FloatField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_zone_boundary'

    def __str__(self):
        return self.zone_name


class MCBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    zone_code = models.ForeignKey(ZoneBoundary, to_field='zone_code', on_delete=models.CASCADE, null=True)
    mc_code = models.CharField(max_length=200, null=True, unique=True)
    mc_name = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    shape_area = models.FloatField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_mc_boundary'

    def __str__(self):
        return self.mc_name


class UnionCouncil(models.Model):
    id = models.AutoField(primary_key=True)
    town_code = models.ForeignKey(TownBoundary, to_field='town_code', on_delete=models.CASCADE, null=True)
    zone_code = models.ForeignKey(ZoneBoundary, to_field='zone_code', on_delete=models.CASCADE, null=True)
    uc_code = models.CharField(max_length=200, null=True, unique=True)
    uc_name = models.TextField(max_length=100, null=True)
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    shape_area = models.FloatField(max_length=200, null=True)
    extent = models.TextField(max_length=200, null=True)
    tehsil_name = models.TextField(max_length=100, null=True)
    district_name = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_union_council_boundary'

    def __str__(self):
        return self.uc_name


class AdministrativeBoundary(models.Model):
    id = models.AutoField(primary_key=True)
    landuse_code = models.ForeignKey(LanduseBoundary, to_field='landuse_code', on_delete=models.CASCADE, null=True)
    admin_code = models.CharField(max_length=200, null=True, unique=True)
    admin_name = models.TextField(max_length=100, null=True)
    admin_type = models.TextField(max_length=200, null=True)  # Union Council, City Council
    geom = models.GeometryField(srid=4326, null=True, blank=True)
    extent = models.TextField(max_length=200, null=True)
    # district_name = models.TextField(max_length=100, null=True)
    status = models.TextField(max_length=200, null=True)  # Active/Block
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_administrative_boundary'

    def __str__(self):
        return self.admin_name
