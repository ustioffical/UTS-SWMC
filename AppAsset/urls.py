from django.urls import re_path
from AppAsset.views import *

urlpatterns = [

    # CONTAINER START
    re_path(r'^Container/Search/', ContainerListView, name='ContainerList'),
    re_path(r'^Container/Create/', CreateContainerView, name='CreateContainer'),

    # # AJAX
    re_path(r'^fetch_drum_feature_data/', FetchDrumFeatureDataView, name='FetchDrumFeatureData'),
    re_path(r'^fetch_container_feature_data/', FetchContainerFeatureDataView, name='FetchContainerFeatureData'),
    re_path(r'^fetch_container_feature_process_type_data/', FetchContainerFeatureData_ProcessTypeView, name='FetchContainerFeatureData_ProcessType'),

    re_path(r'^fetch_collection_site_feature_data/', FetchCollectionSiteDataView, name='FetchCollectionSiteData'),

    re_path(r'^fetch_dumping_site_feature_data/', FetchDumpingSiteDataView, name='FetchDumpingSiteData'),
    re_path(r'^fetch_dumping_coverage_feature_data/', FetchDumpingCoverageDataView, name='FetchDumpingCoverageData'),
    re_path(r'^fetch_weighing_site_feature_data/', FetchWeighingSiteDataView, name='FetchWeighingSiteData'),
    re_path(r'^fetch_weighing_coverage_feature_data/', FetchWeighingCoverageDataView, name='FetchWeighingCoverageData'),

    re_path(r'^fetch_parking_site_feature_data/', FetchParkingSiteDataView, name='FetchParkingSiteData'),
    re_path(r'^fetch_workshop_feature_data/', FetchWorkshopDataView, name='FetchWorkshopData'),
    re_path(r'^fetch_filling_station_feature_data/', FetchFillingStationDataView, name='FetchFillingStationData'),
    # Vehicle last location url
    re_path(r'^vehicle_lastest_location/',VehicleLastLocationView, name='VehicleLastLocation'),

]