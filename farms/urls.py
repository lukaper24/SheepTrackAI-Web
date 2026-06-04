from django.urls import path
from .views import farm_list, farm_create

urlpatterns = [
    path('', farm_list, name='farm_list'),
    path('create/', farm_create, name='farm_create'),
]