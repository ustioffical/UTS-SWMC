from django.http import HttpResponse
from django.shortcuts import render

from AppAdmin.utils import *

# Create your views here.
def DefaultMappingView(request):
    template_name = "Default-Map.html"
    cursor = connections['default'].cursor()

    params = {
        # 'container_feature': container_feature,
        # 'town_boundary': town_boundary,
        # 'feature_lists': feature_lists,
        # 'message': message,
    }

    return render(request, template_name, params)
