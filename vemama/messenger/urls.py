from django.urls import path
from . import views

app_name = "messenger"

urlpatterns = [
    path("1d03e747abc9832543417431adb24fac56be777df43ff2d619", views.MessengerView.as_view(), name="messenger"),
    path("send", views.send_message_view, name="sample_message"),
]
