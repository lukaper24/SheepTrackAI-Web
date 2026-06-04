from django.urls import path
from .views import veterinary_list, veterinary_create, veterinary_delete

urlpatterns = [
    path("", veterinary_list, name="veterinary_list"),
    path("create/", veterinary_create, name="veterinary_create"),
    path("<int:pk>/delete/", veterinary_delete, name="veterinary_delete"),
]