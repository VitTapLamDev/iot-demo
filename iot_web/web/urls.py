from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("sensor_data", views.sensor_data, name="sensor_data"),
    path("data", views.data, name="data"),
    path("data_sensor", views.data_sensor, name="data_sensor")
]
