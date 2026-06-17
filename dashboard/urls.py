from django.urls import path
from .views import home,about, api_dashboard_stats, api_sheep_list,api_lambing_list


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("api/dashboard-stats/", api_dashboard_stats, name="api_dashboard_stats"),
    path("api/sheep/", api_sheep_list, name="api_sheep_list"),
    path("api/lambings/", api_lambing_list, name="api_lambing_list"),
]