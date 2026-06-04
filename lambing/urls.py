from django.urls import path
from .views import (
    lambing_list,
    lambing_create,
    lambing_detail,
    lambing_delete,
    lamb_list,
    lamb_update,
)

urlpatterns = [
    path("", lambing_list, name="lambing_list"),
    path("create/", lambing_create, name="lambing_create"),
    path("lambs/", lamb_list, name="lamb_list"),
    path("lambs/<int:pk>/edit/", lamb_update, name="lamb_update"),
    path("<int:pk>/", lambing_detail, name="lambing_detail"),
    path("<int:pk>/delete/", lambing_delete, name="lambing_delete"),
]