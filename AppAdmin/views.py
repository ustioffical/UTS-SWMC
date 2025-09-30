import json
import datetime

from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse

from AppAdmin.utils import *
from AppAsset.models import *


# Create your views here.
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def DashboardView(request):
    template_name = "Dashboard.html"

    format_str = "%Y-%m-%d %H:%M:%S"
    format_date = '%Y-%m-%d'
    current_data_time = datetime.datetime.now()
    today_date = current_data_time.strftime(format_date)

    # GENERATE CONTAINER PROCESS RECORD IN DATABASE
    RetriveContainProcess = ContainerProcess.objects.filter(created_at__date=today_date)
    if len(RetriveContainProcess) == 0:  # IF RECORD FOUND OR MISSING RECORD CHECK
        GenerateContainerProcessRecordDB_DayWise_Function(today_date)

    return render(request, template_name)


# THIS FUNCTION USED GLOBALLY IN ALL APPLICATION

def FillCmdListByModelView(request):
    table_name = request.POST['table_name']
    column_name = request.POST['column_name']
    column_code = request.POST['column_code']
    model_name = next((m for m in apps.get_models() if m._meta.db_table == table_name), None)

    cmd_list = list(model_name.objects.values(column_code, column_name).order_by(column_name))
    params = {'cmd_list': cmd_list}

    return HttpResponse(json.dumps(params, default=date_handler))


def FillCmdListByModelWithCodeView(request):
    table_name = request.POST['table_name']
    condition_column = request.POST['condition_column']
    condition_split = condition_column.split("=")
    condition_key = condition_split[0]
    condition_value = condition_split[1]

    cmd_column = request.POST['cmd_column']
    column_split = cmd_column.split("^^")
    column_code = column_split[0]
    column_name = column_split[1]

    model_name = next((m for m in apps.get_models() if m._meta.db_table == table_name), None)

    # variable_column = 'name'
    # search_type = 'contains'
    # filter = variable_column + '__' + search_type
    # info = members.filter(**{filter: search_string})

    filter = condition_key
    cmd_list = list(
        model_name.objects.filter(**{filter: condition_value}).values(column_code, column_name).order_by(column_name))
    params = {'cmd_list': cmd_list}

    return HttpResponse(json.dumps(params, default=date_handler))


# ADMIN PYTHON FUNCTION START
# GENERATE CONTAINER PROCESS RECORD IN DATABASE
def GenerateContainerProcessRecordDB_DayWise_Function(today_date):
    ### GET CONTAINER PROCESS
    GetContainerProcessType = ContainerProcessType.objects.get(cont_proc_type_code="CPT-2")
    ReadContainer = ContainerData.objects.all().order_by('id')

    RetriveContainProcess = ContainerProcess.objects.filter(created_at__date=today_date)
    if len(RetriveContainProcess) > 0:  # IF RECORD FOUND OR MISSING RECORD CHECK
        if len(ReadContainer) > 0:  # CONTAINER EXIST
            for c in range(len(ReadContainer)):  # LOOP CONTAINER DATA
                rd_container_code = ReadContainer[c].container_code
                ExistContainerProcess = ContainerProcess.objects.filter(created_at__date=today_date,
                                                                        container_code_id=rd_container_code)
                if len(ExistContainerProcess) == 0:  # NO RECORD FOUND
                    auto_process_code = AutoGenerateCodeForModel(ContainerProcess, "container_process_code", "CP-")
                    # INSERT CONTAINER PROCESS DATA (START)
                    InstContainerProcess = ContainerProcess(
                        container_process_code=auto_process_code,
                        container_code_id=rd_container_code,
                        cont_proc_type_code_id=GetContainerProcessType.cont_proc_type_code,
                        created_at=datetime.datetime.now(),
                        created_by="admin"
                    )
                    InstContainerProcess.save()
                    # TRACKER AND VEHICLE RELATION (END)
                ### NO RECORD FOUND
            ### LOOP END

    else:  # CREATE

        if len(ReadContainer) > 0:  # UPDATE
            for c in range(len(ReadContainer)):
                auto_process_code = AutoGenerateCodeForModel(ContainerProcess, "container_process_code", "CP-")
                # INSERT CONTAINER PROCESS DATA (START)
                InstContainerProcess = ContainerProcess(
                    container_process_code=auto_process_code,
                    container_code_id=ReadContainer[c].container_code,
                    cont_proc_type_code_id=GetContainerProcessType.cont_proc_type_code,
                    created_at=datetime.datetime.now(),
                    created_by="admin"
                )
                InstContainerProcess.save()
                # TRACKER AND VEHICLE RELATION (END)

    ### GET CONTAINER PROCESS

    return True
