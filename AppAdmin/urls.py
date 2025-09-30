from django.urls import re_path
from AppAdmin.views import *

urlpatterns = [
    re_path(r'^Dashboard/', DashboardView, name='Dashboard'),

    # GLOBAL AJAX FUNCTION
    re_path(r'cmd_list_model', FillCmdListByModelView, name='FillCmdListByModel'),
    re_path(r'fill_cmd_model_with_code', FillCmdListByModelWithCodeView, name='FillCmdListByModelWithCode'),

]
