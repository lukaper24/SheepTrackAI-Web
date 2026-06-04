from django.urls import path
from .views import (
    sheep_list,
    sheep_create,
    sheep_detail,
    sheep_update,
    sheep_delete,
)

urlpatterns = [
    path("", sheep_list, name="sheep_list"),
    path("create/", sheep_create, name="sheep_create"),
    path("<int:pk>/", sheep_detail, name="sheep_detail"),
    path("<int:pk>/edit/", sheep_update, name="sheep_update"),
    path("<int:pk>/delete/", sheep_delete, name="sheep_delete"),
]