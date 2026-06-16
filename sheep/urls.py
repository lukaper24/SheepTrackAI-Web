from django.urls import path

from .views import (
    sheep_list,
    sheep_create,
    sheep_detail,
    sheep_update,
    sheep_delete,
    sheep_archive,
    sheep_mark_exit,
    sheep_restore,
    sheep_import_eposjednik,
)

urlpatterns = [
    path("", sheep_list, name="sheep_list"),
    path("create/", sheep_create, name="sheep_create"),
    path("archive/", sheep_archive, name="sheep_archive"),
    path("import/eposjednik/", sheep_import_eposjednik, name="sheep_import_eposjednik"),
    path("<int:pk>/", sheep_detail, name="sheep_detail"),
    path("<int:pk>/edit/", sheep_update, name="sheep_update"),
    path("<int:pk>/delete/", sheep_delete, name="sheep_delete"),
    path("<int:pk>/exit/<str:status>/", sheep_mark_exit, name="sheep_mark_exit"),
    path("<int:pk>/restore/", sheep_restore, name="sheep_restore"),
]