from django.urls import path
from .views import home,about, api_dashboard_stats


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("api/dashboard-stats/", api_dashboard_stats, name="api_dashboard_stats"),
]