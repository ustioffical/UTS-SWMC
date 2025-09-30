from django.urls import re_path
from AppSetting.views import *

urlpatterns = [
    # re_path(r'^Default/', DefaultMappingView, name='Default-Mapping'),

    ### AJAX VIEW
    re_path(r'push_pitb_server_post_vtms_data/', PushDataPITBServer_PostVTMSDataView,
            name='PushDataPITBServer_PostVTMSData'),

    # AJAX
    re_path(r'Pitb/Transmission-List/', PITBApi_TransmissionDataListView, name='PITBApi_TransmissionDataList'),

    ### AJAX VIEW
    re_path(r'push_pitb_server_post_vtms_data/', PushDataPITBServer_PostVTMSDataView,
         name='PushDataPITBServer_PostVTMSData'),

    re_path(r'^fetch_union_council_feature_data/', FetchUnionCouncilFeatureView, name='FetchUnionCouncilFeature'),
    re_path(r'^fetch_landuse_boundary_feature_data/', FetchLanduseBoundaryFeatureView,
            name='FetchLanduseBoundaryFeature'),
    re_path(r'^fetch_admin_boundary_feature_data/', FetchAdministrativeBoundaryFeatureView,
            name='FetchAdministrativeBoundaryFeature'),


]
