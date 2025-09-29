from django.urls import re_path
from AppReport.views import *

urlpatterns = [

    # VEHICLE START

    # CONTAINER START
    re_path(r'^/Vehicle/Route/', VehicleRouteReportView, name='VehicleRouteReport'),
    re_path(r'^/Vehicle/History/', VehicleHistoryReportView, name='VehicleHistoryReport'),
    re_path(r'^/Vehicle/Trip-Report/', VehicleTripHistoryReportView, name='VehicleTripHistoryReport'),
    re_path(r'^/Container/History/', ContainerHistoryReportView, name='ContainerHistoryReport'),

    ### AJAX

    # Fetch OSM Road Network By Filter
    # re_path(r'^fetch_osm_network_by_filter/', FetchOSMRoadNetworkByFilterView, name='FetchOSMRoadNetworkByFilter'),
    # re_path(r'^fetch_route_network_schedule_feature/', FetchRouteNetworkScheduleFeatureView, name='FetchRouteNetworkScheduleFeature'),

]
