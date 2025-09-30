from django.urls import re_path, path, include
from AppVehicle.views import *

urlpatterns = [

    # VEHICLE MONITOR URL
    re_path(r'^Vehicle-Monitor/', AllVehicleMonitoringView, name='AllVehicleMonitoring'),
    ### EXCEL
    re_path('export-excel/', GetVehicleDataExcel, name='export_excel'),

    ### SYNC VEHICLE FROM VENDOR SERVER API URL
    re_path(r'^Vehicle-Sync/', AllVehicleSyncView, name='AllVehicleSync'),

    ### VEHICLE MANAGEMENT URL
    re_path(r'^Vehicle-Management/', AllVehicleManagementView, name='AllVehicleManagement'),

    ### NOT RESPONSE VEHICLE LIST
    path('No-Response-Vehicles/', NoResponseVehicleView, name='no-response-vehicle'),


    # # vehicle_status_details
    re_path(r'^Single-Complete-Info/<str:vehicle_code>/', SingleVehicleCompleteDetailView, name='vehicle-status-details'),

    ### VEHICLE THRESHOLD REPORT ####
    re_path(r'^Report/Threshold/', VehicleThresholdReportView, name='VehicleThresholdReport'),

    ### VEHICLE GEO STATUS REPORT PAGE LIKE MOVING, IDLE, PARK ####
    path('Report/Geo-Status-Movement/', VehicleGeoStatusMovementReportView, name='VehicleGeoStatusMovementReport'),

    path('Report/Geo-Status-Movement/<str:vehicle_code>/', SingleVehicleGeoStatusMovementReportView,
         name='SingleVehicleGeoStatusMovementReport'),

    ### SINGLE VEHICLE FLEET ACTIVITY
    path('Report/Fleet-Activity-Info/<str:pitb_code>/', SingleVehicleFleetActivityReportView,
         name='SingleVehicleFleetActivityReport'),


    ### EXCEL DOWNLOAD
    path('vehicle-threshold/export/', ExportVehicleThresholdExcel, name='export_vehicle_threshold_excel'),

    path('vehicle-threshold/', VehicleThresholdView, name='VehicleThresholdView'),

    path('create-vehicle-threshold/', CreateUpdateVehicleThreshold, name='CreateUpdateVehicleThreshold'),

    # REPORT
   # re_path(r'^Mohid-Route-Report/', VehicleRouteReportMohidView, name='VehicleRouteReportMohid'),


    ### VTMS REPORTS START
    re_path(r'^Vehicle/VTMS-Report/', VTMSReportView, name='VTMSReport'),

    # REPORT EXCEL
    re_path('export-vtms-report-excel/', ExportVTMSReportExcel, name='ExportVTMSReportExcel'),

    # Tracker
    re_path(r'^Vehicle-Tracker-GPRS-Data-Sync/', SyncVehicleTrackerGPRS_RawDataView,
            name='SyncVehicleTrackerGPRS_RawData'),

    # # AJAX
    re_path(r'^fetch_vehicle_feature_data/', FetchVehicleFeatureDataView, name='FetchVehicleFeatureData'),
    re_path(r'^fetch_vehicle_trip_history_data/', FetchVehicleTripHistoryDataView, name='FetchVehicleTripHistoryData'),
    re_path(r'^fetch_vehicle_live_monitoring_GPRS_data/', FetchVehicleLiveMonitoringByGPRSView,
            name='FetchVehicleLiveMonitoringByGPRS'),

    re_path(r'^fetch_single_vehicle_route_data/', FetchSingleVehicleRouteDataView, name='FetchSingleVehicleRouteData'),

    re_path(r'^fetch_single_vehicle_trip_history_data/', FetchSingleVehicleTripHistoryDataView,
            name='FetchSingleVehicleTripHistoryData'),
    re_path(r'^vehicle_list_with_type_code/', VehicleListWithTypeCodeView, name='VehicleListWithTypeCode'),


    path('FetchVehicleCodes/', FetchVehicleCodes, name='get_vehicle_codes'),  # AJAX Endpoint

    # vehicle_status_details
    path('ajax/get_vehicle_vtms_status/', get_vehicle_vtms_status, name='get_vehicle_vtms_status'),
    path('vehicle/update-vtms-status/', update_vehicle_vtms_status, name='update_vehicle_vtms_status'),
    path('connect-vehicle-to-route/', connect_vehicle_to_route, name='connect_vehicle_to_route'),

    path('create-complaint-form/<int:complaint_id>', create_complaint_form_view, name='create_complaint_form'),
    path('manage-complaint/', ViewAndUpdateComplaintsView, name='manage-complaints'),
    path('complaints/<uuid:complaint_id>/', ViewComplaintDetailView, name='getspecificcomplaint'),



    path('connect-vehicle-to-route/', connect_vehicle_to_route, name='connect_vehicle_to_route'),

    path('featch-single-vehicle-route-data-by-date-and-id/', FetchVehicleRouteDataByDateandId, name='FetchVehicleRouteDataByDateandId'),

    ### TRACKER, TELECOM AND VEHICLE CONNECTIVITY URL

    path('Terminal-Data/', TerminalDataView, name='terminal-data'),
    path('Save-Terminal-Data/', SaveTerminalDataView, name='save-terminal-data'),
    path('Update-Terminal-Data/', UpdateTerminalDataView, name='update-terminal-data'),

    path('Telecom-Data/', TelecomDataView, name='telecom-data'),
    path('Update-Telecom-Data/', UpdateTelecomDataView, name='update-telecom-data'),

    path('Tracker-Telecom-Data/', TrackerTelecomDataView, name='tracker-telecom-data'),


    path('vehicle-terminal-pairing/', VehicleTerminalPairingView, name='VehicleTerminalPairingView'),
    path('save-vehicle-terminal-pairing/', SaveVehicleTerminalPairing, name='save_vehicle_terminal_pairing'),

    path('push-to-pitb/', PushToPITB, name='PushToPITB'),


    ### VEHICLE DATA SYSTEM ####
    # ALL VEHICLE DATA
    re_path(r'^All-Lists/', AllVehicleDataViewset, name='AllVehicleData'),
    re_path(r'^Vehicle-Type-Manager/', VehicleTypeManagerView, name='VehicleTypeManager'),

    # Vehicle Used for manager
    re_path(r'^PITB/Used-For-Manager/', VehicleUsedForManagerView, name='VehicleUsedForManager'),

    # Tracker History Report
    # path('TrackerHistory/', TrackerHistoryView, name='tracker-history-view'),
    path('TrackerHistory/', test_view, name='tracker-history-view'),




    # Owner Management
    path('owner-management/', OwnerManagmentView, name='owner_management'),
    # Driver Managment
    path('driver-management/',DriverManagmentView, name='driver_management'),
    # Vehicle Driver Managment
    path('vehicle-driver-management/',VehicleDriverAssignmentView,name='vehicle_driver_management'),
    # PUsh no response vehicle
    path('push_not_response_vehicles/',PushPITBNotResponseVehicleData,name='push_not_response_vehicles'),

# Single Vehicle info
    path('single-vehicle-info/<str:register_no>/', SingleVehicleInfo, name='single_vehicle_info'),

    # Trip Report
    path('TripReport/',TripReportView,name='trip-report-view'),
    path('OfflineTripReport/',OfflineTripReportView,name='offline-trip-report-view'),

    path('vehicle-data-logs/',VehicleDataLogsView,name='vehicle-data-logs'),
]
