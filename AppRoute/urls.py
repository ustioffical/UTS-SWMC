from django.urls import re_path,path
from AppRoute.views import *

urlpatterns = [

    # CONTAINER START
    re_path(r'^Design-Create/', CreateNetworkWithListView, name='CreateNetworkWithList'),
    re_path(r'^Design-Route-Network/', DesignRouteNetworkView, name='DesignRouteNetwork'),

    # AJAX

    # Fetch OSM Road Network By Filter
    re_path(r'^fetch_osm_network_by_filter/', FetchOSMRoadNetworkByFilterView, name='FetchOSMRoadNetworkByFilter'),
    re_path(r'^fetch_route_network_schedule_feature/', FetchRouteNetworkScheduleFeatureView, name='FetchRouteNetworkScheduleFeature'),


]