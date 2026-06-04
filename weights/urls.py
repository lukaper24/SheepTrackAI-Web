from django.urls import path

from .views import (
    weight_list,
    weight_create,
    weight_delete,
)

urlpatterns = [
    path("", weight_list, name="weight_list"),
    path("create/", weight_create, name="weight_create"),
    path("<int:pk>/delete/", weight_delete, name="weight_delete"),
]