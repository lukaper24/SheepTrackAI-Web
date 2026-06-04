from django.urls import path
from .views import sheep_list, sheep_create

urlpatterns = [
    path('', sheep_list, name='sheep_list'),
    path('create/', sheep_create, name='sheep_create'),
]