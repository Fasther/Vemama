from django.urls import path
from core.views import IndexView, ChangePasswordView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('change-password/', ChangePasswordView.as_view(), name="change_password"),
]
