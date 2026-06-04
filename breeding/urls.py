from django.urls import path
from .views import breeding_list, breeding_create, breeding_delete

urlpatterns = [
    path("", breeding_list, name="breeding_list"),
    path("create/", breeding_create, name="breeding_create"),
    path("<int:pk>/delete/", breeding_delete, name="breeding_delete"),
]