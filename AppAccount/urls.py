from django.urls import path
from AppAccount.views import *

urlpatterns = [
    path('', LoginView, name='LoginView'),
    path('logout/', LogoutView, name='LogoutView')
]