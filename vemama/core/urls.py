from django.urls import path
from core.views import IndexView, ChangePasswordView, ResetPassView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('change-password/', ChangePasswordView.as_view(), name="change_password"),
    path('reset-password/', ResetPassView.as_view(), name="reset_password")
]
