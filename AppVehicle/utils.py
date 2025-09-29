from datetime import datetime, timedelta, time

from AppAdmin.utils import *
from AppVehicle.models import *

### GENERATE WORKING SCHEDULA WITH VEHICLE SCHEDULE IN SYSTEM FUNCTION
# def GenerateWorkingWithVehicleSchedule_Function(selected_date):
#     response_message = ""
#     current_data_time = datetime.datetime.now()
#
#     ### GENERATE VEHICLE SCHEDULA IN SYSTEM FUNCTION len(vehicle_list)
#     vehicle_list = list(VehicleData.objects.filter(status="Active").order_by('vehicle_type'))
#     ### IF CURRENT DATE EXIST OR NOT
#     veh_sche_date_records = VehicleScheduleGPRSApi.objects.filter(veh_sch_date=selected_date)
#
#     if len(vehicle_list) == len(veh_sche_date_records):
#         response_message = "Equal Record"
#         return response_message
#     ### IF VEHICLE AND SCHEDULE VEHICLE EQUAL
#
#     ### GENERATE WORKING SCHEDULA
#     qs = WorkScheduleGPRSApi.objects.filter(work_date=selected_date)
#     if not qs.exists():
#         generated_code = AutoGenerateCodeForModel(WorkScheduleGPRSApi, "code", "WS-")
#         new_record = WorkScheduleGPRSApi.objects.create(
#             code=generated_code,
#             work_date=selected_date,
#             run_count=0,
#             process_status="Pending",
#             description="Sync-Current",
#             created_at=current_data_time,
#             created_by="admin"
#         )
#         ws_code = new_record.code
#     else:
#         existing = qs.first()
#         ws_code = existing.code
#
#     ### INSERTED ALL VEHICLE IN SCHEDULA MODEL
#     for v in range(len(vehicle_list)):
#
#         set_vehicle_code = vehicle_list[v].vehicle_code
#         ### IF CURRENT DATE EXIST OR NOT
#         current_date_records = VehicleScheduleGPRSApi.objects.filter(created_at=selected_date,
#                                                                      vehicle_code_id=set_vehicle_code)
#         if len(current_date_records) == 0:  ## IF CURRENT DATE EXIST
#             response_message = "Created Record"
#             auto_vs_code = AutoGenerateCodeForModel(VehicleScheduleGPRSApi, "veh_api_code", "VAI-")
#             ### GPRS - VEHICLE SCHEDULE API (START)
#             InstVehSche = VehicleScheduleGPRSApi(
#                 veh_api_code=auto_vs_code,
#                 vehicle_code_id=set_vehicle_code,
#                 veh_sch_date=selected_date,
#                 wsa_code_id=ws_code,
#                 retrieve_record=0,
#                 vendor_record=0,
#                 process_status="Pending",
#                 created_at=current_data_time,
#                 created_by="admin"
#             )
#             InstVehSche.save()
#     #         ### GPRS - VEHICLE SCHEDULE API (END)
#     #     ### NO RECORD FOUND CONDITION (END)
#     # ### LOOP CONDITION (END)
#
#     return response_message