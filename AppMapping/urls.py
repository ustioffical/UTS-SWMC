from django.urls import re_path
from AppMapping.views import *

urlpatterns = [
    re_path(r'^Default/', DefaultMappingView, name='Default-Mapping'),
]
